#!/usr/bin/env python3
import argparse
import chromadb
import base64
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from typing import List

console = Console()


class ChromaViewer:
    def __init__(self, host: str, port: int, username: str, password: str):
        auth_str = f"{username}:{password}"
        auth_header = f"Basic {base64.b64encode(auth_str.encode()).decode()}"
        self.client = chromadb.HttpClient(
            host=host, port=port, headers={"Authorization": auth_header}, ssl=False
        )

    def list_collections(self) -> List[str]:
        try:
            collections = self.client.list_collections()
            return [str(col) for col in collections]
        except Exception as e:
            console.print(f"Error listing collections: {str(e)}", style="red")
            return []

    def peek_collection(self, collection_name: str, n_items: int = 5) -> None:
        try:
            collection = self.client.get_collection(collection_name)
            result = collection.peek(limit=n_items)

            if not result or not result.get("ids"):
                console.print("Collection is empty", style="yellow")
                return

            table = Table(title=f"Preview of {collection_name}")
            table.add_column("ID", style="cyan")
            table.add_column("Document", style="green")
            table.add_column("Metadata", style="yellow")

            ids = result.get("ids", []) or []
            docs = result.get("documents", []) or []
            metas = result.get("metadatas", []) or []

            for i in range(min(len(ids), len(docs), len(metas))):
                doc_text = str(docs[i])
                displayed_text = (
                    doc_text[:100] + "..." if len(doc_text) > 100 else doc_text
                )
                table.add_row(
                    str(ids[i]), displayed_text, str(metas[i]) if metas[i] else "None"
                )

            console.print(table)
            console.print(
                f"\nTotal items in collection: {collection.count()}", style="blue"
            )

        except Exception as e:
            console.print(f"Error peeking collection: {str(e)}", style="red")

    def show_collection_info(self, collection_name: str) -> None:
        try:
            collection = self.client.get_collection(collection_name)
            count = collection.count()

            table = Table(title=f"Collection: {collection_name}")
            table.add_column("Property", style="cyan")
            table.add_column("Value", style="green")

            table.add_row("Number of items", str(count))
            table.add_row("Metadata", str(collection.metadata))

            console.print(table)
            console.print("\nCollection Preview:", style="blue")
            self.peek_collection(collection_name)

        except Exception as e:
            console.print(f"Error getting collection info: {str(e)}", style="red")


def interactive_mode(viewer: ChromaViewer) -> None:
    while True:
        try:
            console.print("\n=== ChromaDB Viewer ===", style="bold blue")
            console.print("1. List collections")
            console.print("2. View collection details")
            console.print("3. Exit")

            choice = Prompt.ask("Select an option", choices=["1", "2", "3"])

            if choice == "1":
                collections = viewer.list_collections()
                if collections:
                    table = Table(title="Available Collections")
                    table.add_column("Collection Name", style="cyan")
                    for collection in collections:
                        table.add_row(collection)
                    console.print(table)

            elif choice == "2":
                collections = viewer.list_collections()
                if not collections:
                    console.print("No collections found!", style="red")
                    continue

                collection_name = Prompt.ask(
                    "Enter collection name", choices=collections
                )
                viewer.show_collection_info(collection_name)

            elif choice == "3":
                break

        except KeyboardInterrupt:
            console.print("\nExiting...", style="yellow")
            break
        except Exception as e:
            console.print(f"Error: {str(e)}", style="red")


def main() -> None:
    parser = argparse.ArgumentParser(description="ChromaDB CLI Viewer")
    parser.add_argument("--host", required=True, help="ChromaDB host")
    parser.add_argument("--port", type=int, required=True, help="ChromaDB port")
    parser.add_argument("--username", required=True, help="Username for authentication")
    parser.add_argument("--password", required=True, help="Password for authentication")

    args = parser.parse_args()

    try:
        viewer = ChromaViewer(
            host=args.host,
            port=args.port,
            username=args.username,
            password=args.password,
        )

        collections = viewer.list_collections()
        if collections is not None:
            console.print(Panel("Connected to ChromaDB successfully!", style="green"))
            interactive_mode(viewer)
        else:
            console.print("Failed to connect to ChromaDB.", style="red")

    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")


if __name__ == "__main__":
    main()

