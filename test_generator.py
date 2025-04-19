#!/usr/bin/env python
# -*- coding: utf-8 -*-

from document_generator import create_document_from_defaults
import os

def main():
    """Test document generation."""
    print("Генерация тестового документа...")
    
    # Generate a test document
    test_doc_path = create_document_from_defaults()
    print(f"Тестовый документ создан: {test_doc_path}")
    
    # Display file size
    size_bytes = os.path.getsize(test_doc_path)
    size_kb = size_bytes / 1024
    print(f"Размер файла: {size_kb:.2f} KB")
    
    print(f"Документ сохранен по пути: {os.path.abspath(test_doc_path)}")
    print("Для проверки результата откройте сгенерированный документ в любом просмотрщике изображений.")

if __name__ == "__main__":
    main()