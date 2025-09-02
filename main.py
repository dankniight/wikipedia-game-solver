import requests
import time
from collections import deque

WIKIPEDIA_LINKS_URL = "https://en.wikipedia.org/w/api.php?action=query&format=json&prop=links&pllimit=max&titles="

REQUEST_DELAY = 1.0  # 1 second delay between requests

HEADERS = {
    'User-Agent': 'WikiGameSolver/1.0 (https://github.com/dankniight/wikipediaGame; email@example.com)'
}

def get_page_links(page_title):
    url = WIKIPEDIA_LINKS_URL + page_title
    try:
        time.sleep(REQUEST_DELAY)  # Be respectful to Wikipedia's servers
        response = requests.get(url, headers=HEADERS) # Include headers
        response.raise_for_status()
        
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        # Check if the page exists
        page_ids = list(pages.keys())
        if not page_ids or page_ids[0] == "-1":
            print(f"Page '{page_title}' does not exist.")
            return []
        
        links = []
        for page_id in pages:
            page_data = pages[page_id]
            if "links" in page_data:
                for link in page_data["links"]:
                    title = link.get("title", "")
                    # Filter out special pages and keep only standard articles
                    if title and not title.startswith(("Special:", "Wikipedia:", "Category:", "File:", "Template:", "Help:")):
                        links.append(title)
        
        return links
    except Exception as e:
        print(f"Error fetching links for {page_title}: {e}")
        return []

def normalize_title(title):
    # Replace spaces with underscores and strip whitespace
    return title.strip().replace(" ", "_")

def find_shortest_path(start_page, end_page, max_depth=3):
    start_page = normalize_title(start_page)
    end_page = normalize_title(end_page)
    
    print(f"Searching for path from '{start_page}' to '{end_page}'...")
    
    if start_page == end_page:
        return [start_page]
    
    # BFS setup
    queue = deque([(start_page, [start_page])])  # (current_page, path_to_current_page)
    visited = {start_page}
    
    while queue:
        current_page, path = queue.popleft()
        
        # Limit search depth to prevent extremely long searches
        if len(path) > max_depth:
            continue
            
        print(f"Exploring links from: {current_page} (path length: {len(path)})")
        
        # Get all links from the current page
        links = get_page_links(current_page)
        
        for link in links:
            # Normalize the link for comparison
            normalized_link = normalize_title(link)
            
            if normalized_link == end_page:
                # Found the target page
                print(f"Found path to {end_page}!")
                return path + [normalized_link]
            
            if normalized_link not in visited:
                visited.add(normalized_link)
                queue.append((normalized_link, path + [normalized_link]))
                
                # Print progress for long searches
                if len(queue) % 100 == 0:
                    print(f"Queue size: {len(queue)}, Visited pages: {len(visited)}")
    
    # No path found
    return None

def main(start_page=None, end_page=None):
    # If not provided as arguments, ask for input
    if not start_page:
        start_page = input("Enter the starting Wikipedia page title: ")
    if not end_page:
        end_page = input("Enter the target Wikipedia page title: ")
    
    if not start_page or not end_page:
        print("Both page titles are required.")
        return
    
    print(f"\nSearching for the shortest path from '{start_page}' to '{end_page}'...")
    print("(This may take a while due to crawling delays)")
    
    path = find_shortest_path(start_page, end_page)
    
    if path:
        print("\nSolution found!")
        print("Path:")
        for i, page in enumerate(path):
            print(f"{i+1}. {page.replace('_', ' ')}")
        print(f"\nTotal steps: {len(path) - 1}")
    else:
        print("\nNo path found between the given pages.")

# For testing with predefined inputs
if __name__ == "__main__":
    # Example usage:
    # main("Tetris", "Daft Punk")

    main()
