# AUC Archive Chatbot - Usage Examples

## Quick Start

```bash
python auc_archive_chatbot.py
```

## Example Conversations

### 1. Exploring Available Collections

```
📝 You: list collections
🤖 Chatbot: 📚 Available Collections:

• University on the Square, Documenting Egypt's 21st Century Revolution (p15795coll7)
• Voice of America Egypt Radio Recordings (p15795coll51)
• AUC Films and Videos and Historic Egypt (p15795coll23)
• AUC Oral Histories and Reminiscences (p15795coll17)
• AUC Photographs (p15795coll37)
• Arabic Books Collection (p15795coll19)
• Arabic Manuscript Collection (p15795coll52)
• Napoleonic Egypt (p15795coll2)
...and 47 more collections
```

### 2. Browsing a Specific Collection

```
📝 You: browse p15795coll7
🤖 Chatbot: 🔍 Search results from 'University on the Square, Documenting Egypt's 21st Century Revolution':

1. **Demonstrators chanting**
   🔗 https://digitalcollections.aucegypt.edu/digital/collection/p15795coll7/id/345

2. **The Egyptian Revolution**
   🔗 https://digitalcollections.aucegypt.edu/digital/collection/p15795coll7/id/327

3. **Demonstrator holding a banner**
   🔗 https://digitalcollections.aucegypt.edu/digital/collection/p15795coll7/id/367

📊 Showing 10 of 414 total results
```

### 3. Searching Within Collections

```
📝 You: search manuscripts in p15795coll52
🤖 Chatbot: 🔍 Search results from 'Arabic Manuscript Collection':

1. **Al-Kitab al-Muqaddas**
   📅 1859
   🔗 https://digitalcollections.aucegypt.edu/digital/collection/p15795coll52/id/123
```

### 4. Getting Item Details

```
📝 You: item p15795coll7 327
🤖 Chatbot: 📄 Item Details:

**Title:** The Egyptian Revolution
**Subject:** Egypt; Revolutions; Demonstrations
**Format:** Video/mp4
**Description:** Documentary footage of the 2011 Egyptian Revolution

🔗 **View Item:** https://digitalcollections.aucegypt.edu/digital/collection/p15795coll7/id/327
```

### 5. Getting Help

```
📝 You: help
🤖 Chatbot: 🤖 AUC Archive Chatbot Help

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
```

## Available Collections (Highlights)

1. **University on the Square, Documenting Egypt's 21st Century Revolution** - 414 items
2. **AUC Photographs** - Historical photographs
3. **Arabic Manuscript Collection** - Historical Arabic texts
4. **Napoleonic Egypt** - Documents from Napoleon's Egyptian campaign
5. **Marriage Certificates Collection** - Historical marriage documents
6. **AUC Oral Histories and Reminiscences** - Audio recordings
7. **Egyptian Gardens and Horticulture** - Historical botanical materials
8. **Syria Documents** - Historical documents about Syria

## Tips for Effective Use

1. **Start with collections**: Use `list collections` to see what's available
2. **Browse before searching**: Use `browse [collection]` to see sample content
3. **Use specific terms**: More specific search terms yield better results
4. **Collection aliases**: Use the short alias codes (like `p15795coll7`) for faster browsing
5. **Direct links**: All results include clickable links to view items online

## Technical Notes

- The chatbot connects to the live AUC Digital Archive API
- All search results are real-time from the archive
- Links lead directly to the official archive website
- Collection aliases are the technical identifiers used by the CONTENTdm system