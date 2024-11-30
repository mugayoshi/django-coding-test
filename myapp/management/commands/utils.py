from typing import Dict, List
from myapp.models import Content, ContentFile


def create_test_content_with_files(title: str, metadata: Dict, files_count: int, rating: float) -> Content:
    content = Content.objects.create(
        title=title,
        metadata=metadata,
        rating=rating,
    )
    files: List[ContentFile] = []
    for i in range(files_count):
        file = ContentFile.objects.create(
            content=content, file=f"{title}_{i}_file_path")
        files.append(file)

    return content
