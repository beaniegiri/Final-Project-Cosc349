const SERVER = "http://127.0.0.1:5001";

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const fileList = document.getElementById("fileList");
const uploadBtn = document.getElementById("uploadBtn");
const results = document.getElementById("results");
const serverFiles = document.getElementById("serverFiles");
const refreshBtn = document.getElementById("refreshBtn");

let selectedFiles = [];

// Drag and drop events
dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("dragover");
    addFiles(Array.from(e.dataTransfer.files));
});

dropZone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
    addFiles(Array.from(fileInput.files));
    fileInput.value = "";
});

function formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
}

function addFiles(files) {
    files.forEach((file) => {
        if (!selectedFiles.find((f) => f.name === file.name)) {
            selectedFiles.push(file);
        }
    });
    renderFileList();
    uploadBtn.disabled = selectedFiles.length === 0;
}

function renderFileList() {
    fileList.innerHTML = "";
    selectedFiles.forEach((file, index) => {
        const item = document.createElement("div");
        item.className = "file-item";
        item.id = `file-${index}`;
        item.innerHTML = `
            <div class="file-header">
                <span class="file-name">${file.name}</span>
                <span class="file-size">${formatSize(file.size)}</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar" id="bar-${index}"></div>
            </div>
            <div class="file-status" id="status-${index}">Waiting...</div>
        `;
        fileList.appendChild(item);
    });
}

function uploadSingleFile(file, index) {
    return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append("files", file);

        const xhr = new XMLHttpRequest();

        xhr.upload.addEventListener("progress", (e) => {
            if (e.lengthComputable) {
                const pct = Math.round((e.loaded / e.total) * 100);
                document.getElementById(`bar-${index}`).style.width = pct + "%";
                document.getElementById(`status-${index}`).textContent = pct + "%";
            }
        });

        xhr.addEventListener("load", () => {
            if (xhr.status === 200) {
                document.getElementById(`bar-${index}`).classList.add("done");
                document.getElementById(`bar-${index}`).style.width = "100%";
                document.getElementById(`status-${index}`).textContent = "Done";
                resolve(file.name);
            } else {
                document.getElementById(`status-${index}`).textContent = "Failed";
                reject(file.name);
            }
        });

        xhr.addEventListener("error", () => {
            document.getElementById(`status-${index}`).textContent = "Error";
            reject(file.name);
        });

        xhr.open("POST", `${SERVER}/upload`);
        xhr.send(formData);
    });
}

uploadBtn.addEventListener("click", async () => {
    if (selectedFiles.length === 0) return;

    uploadBtn.disabled = true;
    results.innerHTML = "";

    // Upload all files in parallel
    const uploads = selectedFiles.map((file, index) =>
        uploadSingleFile(file, index)
    );

    try {
        const done = await Promise.all(uploads);
        results.innerHTML = `<div class="result-msg success">
            Successfully uploaded ${done.length} file(s): ${done.join(", ")}
        </div>`;
        selectedFiles = [];
        uploadBtn.disabled = true;
        loadServerFiles();
    } catch (err) {
        results.innerHTML = `<div class="result-msg error">
            Some files failed to upload. Please try again.
        </div>`;
        uploadBtn.disabled = false;
    }
});

function loadServerFiles() {
    fetch(`${SERVER}/files`)
        .then((res) => res.json())
        .then((data) => {
            serverFiles.innerHTML = "";
            if (data.files.length === 0) {
                serverFiles.innerHTML = '<li class="empty">No files uploaded yet</li>';
            } else {
                data.files.forEach((name) => {
                    const li = document.createElement("li");
                    li.textContent = name;
                    serverFiles.appendChild(li);
                });
            }
        })
        .catch(() => {
            serverFiles.innerHTML = '<li class="empty">Could not connect to server</li>';
        });
}

refreshBtn.addEventListener("click", loadServerFiles);

// Load server files on page load
loadServerFiles();
