#!/usr/bin/env python3
"""
AUC Archive Chatbot

A chatbot interface for searching and retrieving information from the 
AUC Digital Archive at https://digitalcollections.aucegypt.edu/

Uses the CONTENTdm API to access collection and item metadata.
"""

import requests
import json
import re
from typing import Dict, List, Optional, Any
from urllib.parse import quote


class AUCArchiveAPI:
    """Client for the AUC Digital Archive CONTENTdm API."""
    
    def __init__(self, base_url: str = "https://digitalcollections.aucegypt.edu"):
        self.base_url = base_url
        self.api_url = f"{base_url}/digital/bl/dmwebservices/index.php"
        
    def _make_request(self, function: str, params: List[str] = None, format_type: str = "json") -> Dict[str, Any]:
        """Make a request to the CONTENTdm API."""
        if params is None:
            params = []
        
        # Build the query string
        param_string = "/".join(params) if params else ""
        query = f"{function}/{param_string}/{format_type}" if param_string else f"{function}/{format_type}"
        
        url = f"{self.api_url}?q={query}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            if format_type == "json":
                return response.json()
            else:
                return {"content": response.text}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse JSON response: {str(e)}"}
    
    def get_collections(self) -> Dict[str, Any]:
        """Get list of all collections in the archive."""
        return self._make_request("dmGetCollectionList")
    
    def search_items(self, collection_alias: str, search_terms: str, fields: List[str] = None, 
                    max_records: int = 20) -> Dict[str, Any]:
        """Search for items within a collection."""
        if fields is None:
            fields = ["title", "date", "subjec", "descri"]
        
        # Format search string: field^searchterm^mode^operator
        search_string = f"CISOSEARCHALL^{search_terms}^any^and"
        field_string = "!".join(fields)
        
        params = [
            collection_alias,           # alias
            search_string,             # searchstrings
            field_string,              # fields
            "nosort",                  # sortby
            str(max_records),          # maxrecs
            "1",                       # start
            "0",                       # suppress
            "0",                       # docptr
            "0",                       # suggest
            "0",                       # facets
            "0",                       # showunpub
            "0"                        # denormalizeFacets
        ]
        
        return self._make_request("dmQuery", params)
    
    def get_item_info(self, collection_alias: str, item_id: str) -> Dict[str, Any]:
        """Get detailed metadata for a specific item."""
        return self._make_request("dmGetItemInfo", [collection_alias, item_id])
    
    def get_collection_info(self, collection_alias: str) -> Dict[str, Any]:
        """Get information about a specific collection's fields."""
        return self._make_request("dmGetCollectionFieldInfo", [collection_alias])
    
    def browse_collection(self, collection_alias: str, fields: List[str] = None, 
                         max_records: int = 20) -> Dict[str, Any]:
        """Browse items in a collection (no search filter)."""
        if fields is None:
            fields = ["title", "date", "subjec"]
        
        field_string = "!".join(fields)
        
        params = [
            collection_alias,           # alias
            "0",                       # searchstrings (0 = browse mode)
            field_string,              # fields
            "nosort",                  # sortby
            str(max_records),          # maxrecs
            "1",                       # start
            "0",                       # suppress
            "0",                       # docptr
            "0",                       # suggest
            "0",                       # facets
            "0",                       # showunpub
            "0"                        # denormalizeFacets
        ]
        
        return self._make_request("dmQuery", params)


class AUCArchiveChatbot:
    """Chatbot interface for the AUC Digital Archive."""
    
    def __init__(self):
        self.api = AUCArchiveAPI()
        self.collections = None
        self.collection_lookup = {}
        
    def initialize(self):
        """Initialize the chatbot by loading collection information."""
        print("🏛️  Initializing AUC Archive Chatbot...")
        
        # Load collections
        collections_data = self.api.get_collections()
        if "error" in collections_data:
            print(f"❌ Error loading collections: {collections_data['error']}")
            return False
        
        self.collections = collections_data
        
        # Create lookup dict for collection aliases and names
        for collection in collections_data:
            alias = collection.get('alias', '').lstrip('/')  # Remove leading slash
            name = collection.get('name', '')
            if alias:
                self.collection_lookup[alias.lower()] = alias
                self.collection_lookup[name.lower()] = alias
            
        print(f"✅ Loaded {len(collections_data)} collections")
        return True
    
    def format_search_results(self, results: Dict[str, Any], collection_name: str = "") -> str:
        """Format search results for display."""
        if "error" in results:
            return f"❌ Search error: {results['error']}"
        
        if not results.get('records'):
            return "📭 No items found matching your search criteria."
        
        output = []
        if collection_name:
            output.append(f"🔍 Search results from '{collection_name}':\n")
        else:
            output.append("🔍 Search results:\n")
        
        records = results['records'][:10]  # Limit to first 10 results
        
        for i, record in enumerate(records, 1):
            # Extract metadata from the record
            title = record.get('title', 'Untitled')
            date = record.get('date', 'Date unknown')
            collection_alias = record.get('collection', '')
            pointer = record.get('pointer', '')
            
            # Create item URL
            clean_alias = collection_alias.lstrip('/')  # Remove leading slash
            item_url = f"https://digitalcollections.aucegypt.edu/digital/collection/{clean_alias}/id/{pointer}"
            
            output.append(f"{i}. **{title}**")
            if date and date != 'Date unknown':
                output.append(f"   📅 {date}")
            output.append(f"   🔗 {item_url}")
            output.append("")
        
        total = results.get('pager', {}).get('total', len(records))
        if total > len(records):
            output.append(f"📊 Showing {len(records)} of {total} total results")
        
        return "\n".join(output)
    
    def format_item_details(self, item_data: Dict[str, Any], collection_alias: str) -> str:
        """Format detailed item information for display."""
        if "error" in item_data:
            return f"❌ Error retrieving item: {item_data['error']}"
        
        output = []
        output.append("📄 **Item Details:**\n")
        
        # Title
        title = item_data.get('title', 'Untitled')
        output.append(f"**Title:** {title}")
        
        # Date
        date = item_data.get('date', '')
        if date:
            output.append(f"**Date:** {date}")
        
        # Creator/Author
        creator = item_data.get('creato', item_data.get('creator', ''))
        if creator:
            output.append(f"**Creator:** {creator}")
        
        # Subject
        subject = item_data.get('subjec', item_data.get('subject', ''))
        if subject:
            output.append(f"**Subject:** {subject}")
        
        # Description
        description = item_data.get('descri', item_data.get('description', ''))
        if description:
            output.append(f"**Description:** {description}")
        
        # Format/Type
        format_field = item_data.get('format', item_data.get('type', ''))
        if format_field:
            output.append(f"**Format:** {format_field}")
        
        # Rights
        rights = item_data.get('rights', '')
        if rights:
            output.append(f"**Rights:** {rights}")
        
        # Item URL
        pointer = item_data.get('dmrecord', item_data.get('pointer', ''))
        if pointer:
            clean_alias = collection_alias.lstrip('/')  # Remove leading slash
            item_url = f"https://digitalcollections.aucegypt.edu/digital/collection/{clean_alias}/id/{pointer}"
            output.append(f"\n🔗 **View Item:** {item_url}")
        
        return "\n".join(output)
    
    def process_query(self, user_input: str) -> str:
        """Process a user query and return a response."""
        user_input = user_input.strip().lower()
        
        # Help command
        if user_input in ['help', '?', 'commands']:
            return self.get_help_message()
        
        # List collections
        if 'collections' in user_input or 'list collections' in user_input:
            return self.list_collections()
        
        # Browse collection
        browse_match = re.search(r'browse\s+(.+)', user_input)
        if browse_match:
            collection_name = browse_match.group(1).strip()
            return self.browse_collection(collection_name)
        
        # Check for collection-specific queries
        for collection in self.collections[:10]:  # Check first 10 collections
            collection_name = collection.get('name', '').lower()
            if collection_name and collection_name in user_input:
                alias = collection.get('alias', '').lstrip('/')
                return self.browse_collection(alias)
        
        # Search within specific collection
        search_match = re.search(r'search\s+(.+?)\s+in\s+(.+)', user_input)
        if search_match:
            search_terms = search_match.group(1).strip()
            collection_name = search_match.group(2).strip()
            return self.search_in_collection(search_terms, collection_name)
        
        # General search
        if user_input.startswith('search '):
            search_terms = user_input[7:].strip()
            return self.search_all_collections(search_terms)
        
        # Item details
        item_match = re.search(r'item\s+(\w+)\s+(\w+)', user_input)
        if item_match:
            collection_alias = item_match.group(1)
            item_id = item_match.group(2)
            return self.get_item_details(collection_alias, item_id)
        
        # Default: treat as general search
        return self.search_all_collections(user_input)
    
    def list_collections(self) -> str:
        """List all available collections."""
        if not self.collections:
            return "❌ Collections not loaded. Please restart the chatbot."
        
        output = ["📚 **Available Collections:**\n"]
        
        for collection in self.collections[:20]:  # Limit to first 20
            name = collection.get('name', 'Unknown')
            alias = collection.get('alias', 'unknown').lstrip('/')  # Remove leading slash for display
            secondary = collection.get('secondary', '')
            
            output.append(f"• **{name}** (`{alias}`)")
            if secondary and secondary != '0':
                output.append(f"  └─ Part of: {secondary}")
        
        if len(self.collections) > 20:
            output.append(f"\n📊 Showing 20 of {len(self.collections)} collections")
        
        return "\n".join(output)
    
    def browse_collection(self, collection_name: str) -> str:
        """Browse items in a specific collection."""
        collection_alias = self.find_collection_alias(collection_name)
        if not collection_alias:
            return f"❌ Collection '{collection_name}' not found. Use 'list collections' to see available collections."
        
        results = self.api.browse_collection(collection_alias)
        collection_info = next((c for c in self.collections if c.get('alias') == collection_alias), {})
        collection_display_name = collection_info.get('name', collection_name)
        
        return self.format_search_results(results, collection_display_name)
    
    def search_in_collection(self, search_terms: str, collection_name: str) -> str:
        """Search for items within a specific collection."""
        collection_alias = self.find_collection_alias(collection_name)
        if not collection_alias:
            return f"❌ Collection '{collection_name}' not found. Use 'list collections' to see available collections."
        
        results = self.api.search_items(collection_alias, search_terms)
        collection_info = next((c for c in self.collections if c.get('alias') == collection_alias), {})
        collection_display_name = collection_info.get('name', collection_name)
        
        return self.format_search_results(results, collection_display_name)
    
    def search_all_collections(self, search_terms: str) -> str:
        """Search across all collections."""
        # For now, search in a representative collection or the first available one
        if not self.collections:
            return "❌ No collections available for search."
        
        # Try searching in multiple major collections
        all_results = []
        searched_collections = []
        
        for collection in self.collections[:5]:  # Search first 5 collections
            alias = collection.get('alias', '')
            name = collection.get('name', '')
            
            if alias:
                results = self.api.search_items(alias, search_terms, max_records=5)
                if results.get('records'):
                    all_results.extend(results['records'])
                    searched_collections.append(name)
        
        if not all_results:
            return f"📭 No items found for '{search_terms}' across searched collections."
        
        # Format combined results
        output = [f"🔍 Search results for '{search_terms}' across collections:\n"]
        
        for i, record in enumerate(all_results[:10], 1):
            title = record.get('title', 'Untitled')
            date = record.get('date', '')
            collection_alias = record.get('collection', '')
            pointer = record.get('pointer', '')
            
            clean_alias = collection_alias.lstrip('/')  # Remove leading slash
            item_url = f"https://digitalcollections.aucegypt.edu/digital/collection/{clean_alias}/id/{pointer}"
            
            output.append(f"{i}. **{title}**")
            if date:
                output.append(f"   📅 {date}")
            output.append(f"   📚 Collection: {collection_alias}")
            output.append(f"   🔗 {item_url}")
            output.append("")
        
        output.append(f"📊 Searched in: {', '.join(searched_collections[:3])}")
        if len(searched_collections) > 3:
            output.append(f" and {len(searched_collections) - 3} more collections")
        
        return "\n".join(output)
    
    def get_item_details(self, collection_alias: str, item_id: str) -> str:
        """Get detailed information about a specific item."""
        item_data = self.api.get_item_info(collection_alias, item_id)
        return self.format_item_details(item_data, collection_alias)
    
    def find_collection_alias(self, collection_name: str) -> Optional[str]:
        """Find collection alias by name or partial match."""
        collection_name = collection_name.lower().strip()
        
        # Exact match
        if collection_name in self.collection_lookup:
            return self.collection_lookup[collection_name]
        
        # Partial match
        for key, alias in self.collection_lookup.items():
            if collection_name in key or key in collection_name:
                return alias
        
        return None
    
    def get_help_message(self) -> str:
        """Return help message with available commands."""
        return """
🤖 **AUC Archive Chatbot Help**

**Commands:**
• `list collections` - Show all available collections
• `browse [collection]` - Browse items in a collection
• `search [terms]` - Search across all collections
• `search [terms] in [collection]` - Search within specific collection
• `item [collection] [id]` - Get details for specific item
• `help` - Show this help message

**Examples:**
• `search Ottoman Empire`
• `browse manuscripts`
• `search architecture in photographs`
• `item manuscripts 1234`

**Tips:**
• Use collection names or aliases (shown in parentheses)
• Search terms can be multiple words
• Results include direct links to view items online
        """.strip()


def main():
    """Main chatbot loop."""
    print("🏛️  Welcome to the AUC Archive Chatbot!")
    print("This chatbot helps you search and explore the AUC Digital Archive.")
    print("Type 'help' for available commands or 'quit' to exit.\n")
    
    chatbot = AUCArchiveChatbot()
    
    # Initialize the chatbot
    if not chatbot.initialize():
        print("❌ Failed to initialize chatbot. Please check your internet connection.")
        return
    
    print("\n✅ Chatbot ready! What would you like to explore?\n")
    
    while True:
        try:
            user_input = input("📝 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for exploring the AUC Archive!")
                break
            
            if not user_input:
                continue
            
            print("🤖 Chatbot: ", end="")
            response = chatbot.process_query(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye! Thanks for exploring the AUC Archive!")
            break
        except Exception as e:
            print(f"❌ An error occurred: {str(e)}")
            print("Please try again or type 'help' for available commands.\n")


if __name__ == "__main__":
    main()