<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>提取电费通知单数据</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    .container { max-width: 600px; margin: auto; text-align: center; }
    .progress { width: 100%; background: #f3f3f3; margin-top: 20px; height: 20px; }
    .progress-bar { height: 20px; background: #4caf50; width: 0; }
    #output { margin-top: 20px; }
    .file-list { text-align: left; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="container">
    <h1>提取电费通知单数据</h1>
    <p>上传或拖拽多个 PDF 文件进行处理。</p>
    <input type="file" id="file-input" multiple accept="application/pdf" />
    <button id="process-btn">处理文件</button>
    <div class="progress">
      <div class="progress-bar" id="progress-bar"></div>
    </div>
    <div id="output"></div>
    <div class="file-list" id="file-list"></div>
  </div>
  <script>
    const fileInput = document.getElementById('file-input');
    const processBtn = document.getElementById('process-btn');
    const progressBar = document.getElementById('progress-bar');
    const output = document.getElementById('output');
    const fileList = document.getElementById('file-list');

    processBtn.addEventListener('click', async () => {
      const files = fileInput.files;
      if (!files.length) {
        alert('请选择一个或多个 PDF 文件！');
        return;
      }

      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
      }

      const apiEndpoint = 'https://your-api-host.com/process-pdfs/';
      output.innerHTML = '处理中，请稍候...';
      progressBar.style.width = '0%';

      try {
        const response = await fetch(apiEndpoint, {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = url;
          a.download = 'extracted_data_all.xlsx';
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(url);
          output.innerHTML = '处理完成！点击下载合并的 Excel 文件。';
          progressBar.style.width = '100%';
        } else {
          output.innerHTML = '处理失败，请重试！';
        }
      } catch (error) {
        output.innerHTML = '请求失败，请检查网络连接！';
      }
    });

    fileInput.addEventListener('change', () => {
      fileList.innerHTML = '';
      for (const file of fileInput.files) {
        fileList.innerHTML += `<li>${file.name}</li>`;
      }
    });
  </script>
</body>
</html>
