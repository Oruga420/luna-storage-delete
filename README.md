# OpenAI Vector Store Deletion Tool

A simple command-line tool to delete OpenAI vector stores individually or in batch.

## Features

- Delete single or multiple vector stores
- Comma-separated input for multiple IDs
- 2-second cooldown between deletions to avoid rate limiting
- Confirmation prompt before deletion
- Detailed progress and status reporting

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/luna-storage-delete.git
cd luna-storage-delete
```

2. Install the required packages:
```bash
pip install openai python-dotenv
```

3. Create a `.env` file in the project directory and add your OpenAI API key:
```
LUNAS_OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

Run the script:
```bash
python delete_vector_stores.py
```

When prompted, enter your vector store IDs separated by commas:
```
vs_123, vs_456, vs_789
```

The script will:
1. Show you all the IDs it's going to delete
2. Ask for confirmation
3. Delete each vector store one by one
4. Wait 2 seconds between each deletion
5. Show progress and status for each deletion

## Error Handling

- The script will show detailed error messages if a deletion fails
- It will continue with the remaining IDs even if one fails
- The 2-second cooldown applies even after errors to maintain rate limiting

## Requirements

- Python 3.6+
- OpenAI Python package
- python-dotenv 