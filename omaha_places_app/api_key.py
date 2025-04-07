from urllib.parse import unquote

def replace_api_key(image_url, api_key):
    '''
    Function to replace the placeholder "GOOGLE_API_KEY" with the actual API key.
    Also adjusts the maxwidth parameter to 900.
    '''

    image_url = image_url.replace('GOOGLE_API_KEY', api_key)
    image_url = image_url.replace('maxwidth=400', 'maxwidth=900')
    image_url = unquote(image_url)

    return image_url