from neo4j import GraphDatabase
from openai import OpenAI
from typing import Dict, List, Tuple
import numpy as np
from .destination import Destination


class Retriever:
    def __init__(self, open_ai_api_key: str, destination: Destination, **kwargs):
        self.openai_client = OpenAI(api_key=open_ai_api_key)
        self.session = destination.get_session()
        self.additional_params = kwargs

    def find_similar_items(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        """Find similar items using vector similarity search."""
        query_embedding = self._get_embedding(query)
        norm_query_embedding = query_embedding / np.linalg.norm(query_embedding)
        result = self.session.run("""
            MATCH (i)
            WHERE i.embedding IS NOT NULL
            WITH i,
                 reduce(dot = 0.0, j in range(0, size($embedding)-1) |
                    dot + $embedding[j] * i.embedding[j]) /
                 (sqrt(reduce(norm1 = 0.0, j in range(0, size($embedding)-1) |
                    norm1 + $embedding[j] * $embedding[j])) *
                  sqrt(reduce(norm2 = 0.0, j in range(0, size(i.embedding)-1) |
                    norm2 + i.embedding[j] * i.embedding[j]))) as similarity
            ORDER BY similarity DESC
            LIMIT $top_k
            RETURN i.text as item, similarity as score
        """, embedding=norm_query_embedding, top_k=top_k)

        return [(record["item"], record["score"]) for record in result]

    def get_immediate_neighbors(self, items: List[Tuple[str, float]]):
        """Retrieve immediate neighbors for each similar item, matching any relationship type."""
        neighbors_dict = {}

        for item, _ in items:
            result = self.session.run("""
                MATCH (i {text: $item})-[r]->(neighbor)
                RETURN DISTINCT neighbor.text AS neighbor
                UNION
                MATCH (i {text: $item})<-[r]-(neighbor)
                RETURN DISTINCT neighbor.text AS neighbor
            """, item=item)

            neighbors_dict[item] = [record["neighbor"] for record in result]

        return neighbors_dict

    def get_immediate_neighbors_with_types(
            self, items: List[Tuple[str, float]], rel_types: List[str]) -> Dict[str, List[str]]:
        neighbors_dict = {}

        rel_pattern = '|'.join(rel_types)

        query = f"""
        MATCH (i {{text: $item}})-[r:{rel_pattern}]->(neighbor)
        RETURN DISTINCT neighbor.text AS neighbor
        UNION
        MATCH (i {{text: $item}})<-[r:{rel_pattern}]-(neighbor)
        RETURN DISTINCT neighbor.text AS neighbor
        """

        try:
            for item, _ in items:
                result = self.session.run(
                    query,
                    item=item
                )
                neighbors_dict[item] = [record["neighbor"] for record in result]

        except Exception as e:
            print(f"Error executing Neo4j query: {str(e)}")
            raise

        return neighbors_dict

    def _get_embedding(self, text: str, model: str = "text-embedding-3-small") -> np.ndarray:
        response = self.openai_client.embeddings.create(
            input=text,
            model=model
        )
        return np.array(response.data[0].embedding)
