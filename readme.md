prefix: http://localhost:5000

```
上传pdf文档
url: /api/upload_pdf
method: post

body: {
    file: 
}

返回结果
{
    file_url: string,
    pdf_path: string
}

说明
file_url为http://localhost:5000/view_pdf/{filename}
pdf_path为"upload/pdf/{filename}
```

```
获取文档每页的数据
url: /api/get_pdf_pages
method: get
params: pdf_path:string

返回结果
[
    {
        total_pages:
        current_page:
        image_data:
    },
    ...
]

说明
image_data为图片的base64编码，可将该值直接作为img标签src的值
```

```
使用豆包视觉模型，进行pdf总结摘要

url: /api/get_summary
method: post
Conten-Type: application/json
body {
    img_data:string
}
说明：img_data为图片的base64编码
返回结果
{
    summary:string
}
```
