import requests
import time
from typing import Dict, Optional

BASE_URL = 'https://adamwapi.vercel.app'
API_KEY = 'YOUR_API_KEY'  # Replace with your API key from https://adamwapi.vercel.app

class AdamWAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def create_research(self, 
                       query: str, 
                       max_tokens: int = 8000,
                       reasoning: bool = False,
                       language: str = 'es') -> Dict:
        """
        Create a new research

        Args:
            query: Query text
            max_tokens: Maximum tokens to use (default: 8000)
            reasoning: Whether to use the reasoning model (default: False)
            language: Response language ('es' or 'en', default: 'es')

        Returns:
            Dict with the API response including the research_id
        """
        try:
            response = requests.post(
                f'{BASE_URL}/api/public/v1/agent/research/create',
                headers=self.headers,
                json={
                    "text": query,
                    "max_tokens": max_tokens,
                    "reasoning": reasoning,
                    "language": language
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al crear investigación: {e}")
            return None

    def get_status(self, research_id: str) -> Optional[str]:
        """
        Gets the status of an investigation

        Args:
            research_id: ID of the investigation

        Returns:
            Status of the investigation or None if there is an error
        """
        try:
            response = requests.get(
                f'{BASE_URL}/api/v1/public/agent/research/{research_id}/status',
                headers=self.headers
            )
            response.raise_for_status()
            result = response.json()
            data = result.get('data', {})
            return data.get('status')
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener estado: {e}")
            return None

    def get_research(self, research_id: str) -> Dict:
        """
        Gets the results of a completed investigation

        Args:
            research_id: Research ID

        Returns:
            Dict with the results of the investigation
        """
        try:
            response = requests.get(
                f'{BASE_URL}/api/v1/public/agent/research/{research_id}',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener resultados: {e}")
            return None

# Example of use
def main():
    # Initialize client
    client = AdamWAPI(API_KEY)
    
    # Create a research
    query = "What is Apple's position compared to its competitors in the technology market?"
    result = client.create_research(query)
    
    if not result:
        return
        
    result2 = result['data']
    research_id = result2['research_id']
    print(f"Research created with ID: {research_id}")
    
    # Esperar a que se complete
    while True:
        status = client.get_status(research_id)
        print(f"State: {status}")
        
        if status == 'completed':
            break
        elif status in ['failed', None]:
            print("Error in the investigation")
            return
            
        time.sleep(5)  # Esperar 5 segundos antes de consultar de nuevo
    
    # Obtener resultados
    research = client.get_research(research_id)
    if research:
        print("\nResearch results:")
        markdown = research['data']
        print(markdown['markdown'])
        stats = research['data']
        stats = stats['stats']
        print("\nToken Statistics:")
        print(f"Input Tokens: {stats['total_input_tokens']}")
        print(f"Output Tokens: {stats['total_output_tokens']}")
        print(f"Total tokens: {stats['total_tokens']}")

if __name__ == "__main__":
    main()