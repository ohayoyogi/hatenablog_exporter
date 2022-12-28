import os
import sys
from pathlib import Path

from hatenablog_exporter.hatenablog import HatenaBlog


def main(hatena_id: str, api_key: str, blog_id: str):
    output_dir = Path(os.getcwd()) / "out"

    os.makedirs(str(output_dir), exist_ok=True)

    blog = HatenaBlog(hatena_id, api_key, blog_id)
    articles = blog.getall(0)

    for article in articles:
        article_dir = output_dir / article.id
        article_dir.mkdir(exist_ok=True, parents=True)

        article_content = article_dir / 'content.md'
        with article_content.open('w') as f:
            f.write(article.content)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
