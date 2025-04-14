
import os
import glob
import frontmatter
import json
from datetime import datetime

def update_posts_json():
    posts = []

    md_files = sorted(glob.glob("posts/*.md"), key=os.path.getmtime, reverse=True)

    for i, filepath in enumerate(md_files, start=1):
        with open(filepath) as f:
            post = frontmatter.load(f)

        metadata = post.metadata

        if not all(key in metadata for key in ['title', 'date', 'excerpt']):
            print(f"Skipping {filepath} - missing required metadata")
            continue

        date = metadata['date']
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                print(f"Skipping {filepath} - invalid date format: {date}")
                continue

        posts.append({
            "id": i,  
            "title": metadata['title'],
            "date": date.strftime('%Y-%m-%d'),
            "excerpt": metadata['excerpt'],
            "filename": os.path.basename(filepath)
        })

    with open('posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"Updated posts.json with {len(posts)} entries.")

if __name__ == '__main__':
    update_posts_json()
