# AUC Archive Chatbot

A chatbot interface for searching and retrieving information from the AUC Digital Archive at [https://digitalcollections.aucegypt.edu/](https://digitalcollections.aucegypt.edu/).

This chatbot uses the CONTENTdm API to provide natural language access to the archive's collections and items.

## Features

- 🔍 **Search Collections**: Search across all collections or within specific collections
- 📚 **Browse Collections**: List and browse available collections
- 📄 **Item Details**: Get detailed metadata for specific items
- 🔗 **Direct Links**: Get direct links to view items in the online archive
- 💬 **Natural Language**: Ask questions in plain English

## Installation

### Prerequisites

- Python 3.7 or higher
- Internet connection (to access the AUC Digital Archive API)

### Setup

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the test script** to verify API connectivity:
   ```bash
   python test_api.py
   ```

4. **Start the chatbot**:
   ```bash
   python auc_archive_chatbot.py
   ```

## Usage

### Search Functionality

The chatbot offers powerful search capabilities that allow you to explore the AUC Digital Archive using natural language queries. Here's how to use the search features:

#### Basic Search
- Use the `search` command followed by your query terms to search across all collections
- Example: `search ancient egypt`

#### Collection-Specific Search
- To search within a specific collection, use the `search in` syntax
- Example: `search ancient egypt in photos`
- You can use either the collection name or its alias (in parentheses) when searching

#### Search Tips
1. **Natural Language Support**
   - Ask questions in plain English
   - The chatbot understands context and relationships between terms
   - Example: "Show me photos of ancient Egyptian architecture"

2. **Collection Navigation**
   - Use `list collections` to see all available collections
   - Each collection has a unique alias (shown in parentheses) that can be used in searches
   - Example: `list collections` will show you all available collections and their aliases

3. **Item Details**
   - Once you find an item you're interested in, use the `item` command to get more details
   - Format: `item [collection] [id]`
   - Example: `item photos 1234`

4. **Best Practices**
   - Start with general terms and refine your search
   - Use collection-specific searches for more targeted results
   - Check the collection aliases when searching specific collections
   - Use quotes for exact phrase matching

### Available Commands

- `list collections` - Show all available collections and their aliases
- `browse [collection]` - Browse items in a collection
- `search [terms]` - Search across all collections
- `search [terms] in [collection]` - Search within specific collection
- `item [collection] [id]` - Get detailed metadata for specific item
- `help` - Show help message
- `quit` - Exit the chatbot

### Example Interactions

```
📝 You: list collections
🤖 Chatbot: 📚 Available Collections:

• **Rare Books and Special Collections Library Digital Archive** (`rbscl`)
• **Archival Photograph Collection** (`photos`)
• **Manuscripts and Archives** (`manuscripts`)
...

📝 You: search Ottoman Empire
🤖 Chatbot: 🔍 Search results for 'Ottoman Empire' across collections:

1. **Ottoman Empire and the Eastern Question**
   📅 1876
   📚 Collection: manuscripts
   🔗 https://digitalcollections.aucegypt.edu/digital/collection/manuscripts/id/1234

📝 You: browse manuscripts
🤖 Chatbot: 🔍 Search results from 'Manuscripts and Archives':

1. **Letter from Cairo**
   📅 1923-05-15
   🔗 https://digitalcollections.aucegypt.edu/digital/collection/manuscripts/id/5678
...

📝 You: search architecture in photos
🤖 Chatbot: 🔍 Search results from 'Archival Photograph Collection':

1. **Islamic Architecture in Cairo**
   📅 1890-1920
   🔗 https://digitalcollections.aucegypt.edu/digital/collection/photos/id/9012
...
```

## API Reference

The chatbot uses the [CONTENTdm API](https://help.oclc.org/Metadata_Services/CONTENTdm/Advanced_website_customization/API_Reference/CONTENTdm_API) to access the AUC Digital Archive. Key API endpoints include:

- `dmGetCollectionList` - Get list of collections
- `dmQuery` - Search and browse items
- `dmGetItemInfo` - Get item metadata
- `dmGetCollectionFieldInfo` - Get collection field information

## Architecture

### Main Components

1. **`AUCArchiveAPI`** - Client class for CONTENTdm API interactions
2. **`AUCArchiveChatbot`** - Main chatbot interface and query processing
3. **Response Formatting** - Methods to format search results and item details

### File Structure

```
AUCArchive/
├── auc_archive_chatbot.py    # Main chatbot implementation
├── test_api.py               # API connectivity test
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## Troubleshooting

### Common Issues

1. **Python not found**
   - Install Python 3.7+ from [python.org](https://python.org)
   - On Windows, use the py launcher: `py auc_archive_chatbot.py`

2. **Network/API errors**
   - Check internet connection
   - Verify the AUC Digital Archive is accessible
   - Run `python test_api.py` to diagnose API issues

3. **No search results**
   - Try different search terms
   - Use `list collections` to see available collections
   - Some collections may be empty or have limited metadata

4. **Slow responses**
   - The API may be slow depending on server load
   - Large collections may take time to search

## Contributing

Feel free to contribute improvements:

1. Add more sophisticated natural language processing
2. Implement faceted search capabilities
3. Add support for downloading items
4. Improve error handling and user experience
5. Add support for compound objects (multi-page items)

## API Documentation

For more information about the CONTENTdm API used by this chatbot:
- [CONTENTdm API Reference](https://help.oclc.org/Metadata_Services/CONTENTdm/Advanced_website_customization/API_Reference/CONTENTdm_API)
- [CONTENTdm Server API Functions](https://help.oclc.org/Metadata_Services/CONTENTdm/Advanced_website_customization/API_Reference/CONTENTdm_API/CONTENTdm_Server_API_Functions_dmwebservices)

## License

This project is open source. Please respect the terms of use of the AUC Digital Archive when using this chatbot.

## Contact

For questions about the AUC Digital Archive content, please contact the AUC Library.
For technical issues with this chatbot, please file an issue in this repository.