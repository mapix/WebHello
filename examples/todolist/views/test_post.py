# -*- coding:utf-8 -*-

def test_post(request):
    if 'upload' in request.files:
        if "image/jpeg" == request.get_upload_type('upload'):
            with open("static/upload.jpg", 'wb') as f:
                f.write(request.get_upload_content('upload'))
            return """<img src="/static/upload.jpg">"""
    return """<form method="post" enctype="multipart/form-data">
<input type="file" name="upload">
<input type="submit">
</form>"""
