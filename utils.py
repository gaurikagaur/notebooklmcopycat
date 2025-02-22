def validate_file(file):
    """
    Validate uploaded file size and type
    """
    # Check file size (max 10MB)
    MAX_SIZE = 10 * 1024 * 1024  # 10MB in bytes
    
    if file.size > MAX_SIZE:
        return False
    
    # Check file extension
    valid_extensions = ['pdf', 'docx', 'txt']
    file_extension = get_file_extension(file.name)
    
    return file_extension in valid_extensions

def get_file_extension(filename):
    """
    Get file extension from filename
    """
    return filename.split('.')[-1].lower()
