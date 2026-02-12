// const API_BASE = "http://127.0.0.1:8000/admin";

// const apiKeyInput = document.getElementById("apiKey");
// const verifyBtn = document.getElementById("verifyBtn");
// const authStatus = document.getElementById("authStatus");
// const adminActions = document.getElementById("adminActions");

// const uploadPdfBtn = document.getElementById("uploadPdfBtn");
// const ingestWebsiteBtn = document.getElementById("ingestWebsiteBtn");
// const refreshSourcesBtn = document.getElementById("refreshSourcesBtn");
// const sourcesList = document.getElementById("sourcesList");

// let ADMIN_KEY = "";

// /* 🔔 Toast */
// function showToast(msg, success = true) {
//   const toast = document.getElementById("toast");
//   toast.textContent = msg;
//   toast.style.background = success ? "#16a34a" : "#dc2626";
//   toast.style.display = "block";
//   setTimeout(() => toast.style.display = "none", 3000);
// }

// /* 🔐 VERIFY KEY */
// verifyBtn.onclick = async () => {
//   const key = apiKeyInput.value.trim();
//   if (!key) return;

//   verifyBtn.disabled = true;
//   verifyBtn.textContent = "Verifying…";

//   try {
//     const res = await fetch(`${API_BASE}/sources`, {
//       headers: { "x-api-key": key }
//     });

//     if (!res.ok) throw new Error();

//     ADMIN_KEY = key;
//     authStatus.textContent = "Admin verified ✅";
//     authStatus.className = "status ok";
//     adminActions.classList.remove("locked");
//     showToast("Admin authenticated");

//     loadSources();

//   } catch {
//     ADMIN_KEY = "";
//     authStatus.textContent = "Invalid admin key ❌";
//     authStatus.className = "status err";
//     adminActions.classList.add("locked");
//     showToast("Invalid admin key", false);
//   }

//   verifyBtn.disabled = false;
//   verifyBtn.textContent = "Verify Key";
// };

// /* 🔧 ADMIN FETCH */
// async function adminFetch(url, options = {}) {
//   options.headers = {
//     ...(options.headers || {}),
//     "x-api-key": ADMIN_KEY
//   };

//   const res = await fetch(url, options);
//   if (!res.ok) throw new Error();
//   return res.json();
// }

// /* 📚 LOAD SOURCES */
// async function loadSources() {
//   sourcesList.innerHTML = "";
//   const sources = await adminFetch(`${API_BASE}/sources`);

//   sources.forEach(s => {
//     const li = document.createElement("li");
//     li.innerHTML = `
//       ${s.source_name}
//       <button class="delete-btn">Delete</button>
//     `;
//     li.querySelector("button").onclick = () => deleteSource(s.source_name);
//     sourcesList.appendChild(li);
//   });
// }

// /* 🗑️ DELETE SOURCE */
// async function deleteSource(name) {
//   await adminFetch(`${API_BASE}/delete/source?source_name=${encodeURIComponent(name)}`, {
//     method: "DELETE"
//   });
//   showToast("Source deleted");
//   loadSources();
// }

// /* 📄 UPLOAD DOCUMENT */
// uploadPdfBtn.onclick = async () => {
//   const file = document.getElementById("pdfFile/docs").files[0];
//   if (!file) return;

//   uploadPdfBtn.textContent = "Uploading…";

//   const form = new FormData();
//   form.append("file", file);

//   await fetch(`${API_BASE}/ingest/pdf/docs`, {
//     method: "POST",
//     headers: { "x-api-key": ADMIN_KEY },
//     body: form
//   });

//   showToast("PDF/docs ingested");
//   uploadPdfBtn.textContent = "Upload PDF/docs";
//   loadSources();
// };

// /* 🌐 WEBSITE */
// ingestWebsiteBtn.onclick = async () => {
//   const url = document.getElementById("websiteUrl").value.trim();
//   if (!url) return;

//   ingestWebsiteBtn.textContent = "Ingesting…";

//   await adminFetch(`${API_BASE}/ingest/website?base_url=${encodeURIComponent(url)}`, {
//     method: "POST"
//   });

//   showToast("Website ingested");
//   ingestWebsiteBtn.textContent = "Ingest Website";
//   loadSources();
// };

// refreshSourcesBtn.onclick = loadSources;


// document.addEventListener("keydown", (e) => {
//   if (e.key === "Enter") {
//     e.preventDefault();
//   }
// });
const API_BASE = "http://127.0.0.1:8000/admin";

const apiKeyInput = document.getElementById("apiKey");
const verifyBtn = document.getElementById("verifyBtn");
const authStatus = document.getElementById("authStatus");
const adminActions = document.getElementById("adminActions");

const uploadPdfBtn = document.getElementById("uploadPdfBtn");
const ingestWebsiteBtn = document.getElementById("ingestWebsiteBtn");
const refreshSourcesBtn = document.getElementById("refreshSourcesBtn");
const sourcesList = document.getElementById("sourcesList");

let ADMIN_KEY = "";

/* 🔔 Toast */
function showToast(msg, success = true) {
  const toast = document.getElementById("toast");
  toast.textContent = msg;
  toast.style.background = success ? "#16a34a" : "#dc2626";
  toast.style.display = "block";
  setTimeout(() => (toast.style.display = "none"), 3000);
}

/* 🔐 SAVE ADMIN KEY */
verifyBtn.onclick = async () => {
  const key = apiKeyInput.value.trim();
  if (!key) return;

  verifyBtn.disabled = true;
  verifyBtn.textContent = "Saving…";

  // We don’t “verify” yet – backend will decide
  ADMIN_KEY = key;
  authStatus.textContent = "Admin key saved 🔐";
  authStatus.className = "status ok";
  adminActions.classList.remove("locked");

  showToast("Admin key saved");

  // Try loading sources to confirm validity
  try {
    await loadSources();
  } catch {
    ADMIN_KEY = "";
    adminActions.classList.add("locked");
    authStatus.textContent = "Invalid admin key ❌";
    authStatus.className = "status err";
    showToast("Invalid admin key", false);
  }

  verifyBtn.disabled = false;
  verifyBtn.textContent = "Verify Key";
};

/* 🔧 ADMIN FETCH */
async function adminFetch(url, options = {}) {
  options.headers = {
    ...(options.headers || {}),
    "x-api-key": ADMIN_KEY
  };

  const res = await fetch(url, options);
  if (!res.ok) {
    if (res.status === 401) {
      throw new Error("Unauthorized");
    }
    throw new Error("Request failed");
  }
  return res.json();
}

/* 📚 LOAD SOURCES */
async function loadSources() {
  sourcesList.innerHTML = "";
  const sources = await adminFetch(`${API_BASE}/sources`);

  if (!sources.length) {
    sourcesList.innerHTML = "<li>No sources yet</li>";
    return;
  }

  sources.forEach(s => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span>${s.source_name}</span>
      <button class="delete-btn">Delete</button>
    `;
    li.querySelector("button").onclick = () => deleteSource(s.source_name);
    sourcesList.appendChild(li);
  });
}

/* 🗑️ DELETE SOURCE */
async function deleteSource(name) {
  await adminFetch(
    `${API_BASE}/delete/source?source_name=${encodeURIComponent(name)}`,
    { method: "DELETE" }
  );
  showToast("Source deleted");
  loadSources();
}
/* 📄 UPLOAD DOCUMENT (PDF / DOCX / TXT) */
uploadPdfBtn.onclick = async () => {
  if (!ADMIN_KEY) {
    showToast("Admin not authenticated", false);
    return;
  }

  const fileInput = document.getElementById("docFile");
  const file = fileInput.files[0];

  if (!file) {
    showToast("Please select a document first", false);
    return;
  }

  uploadPdfBtn.disabled = true;
  uploadPdfBtn.textContent = "Uploading…";

  try {
    const form = new FormData();
    form.append("file", file);

    const res = await fetch(`${API_BASE}/ingest/document`, {
      method: "POST",
      headers: {
        "x-api-key": ADMIN_KEY
      },
      body: form
    });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(err);
    }

    showToast("Document ingested successfully ✅");
    fileInput.value = ""; // reset
    loadSources();

  } catch (err) {
    console.error(err);
    showToast("Document ingestion failed ❌", false);
  } finally {
    uploadPdfBtn.disabled = false;
    uploadPdfBtn.textContent = "Upload Document";
  }
};

/* 🌐 WEBSITE INGESTION */
ingestWebsiteBtn.onclick = async () => {
  const url = document.getElementById("websiteUrl").value.trim();
  if (!url) return;

  ingestWebsiteBtn.disabled = true;
  ingestWebsiteBtn.textContent = "Ingesting…";

  try {
    await adminFetch(
      `${API_BASE}/ingest/website?base_url=${encodeURIComponent(url)}`,
      { method: "POST" }
    );
    showToast("Website ingested");
    loadSources();
  } catch {
    showToast("Website ingestion failed", false);
  } finally {
    ingestWebsiteBtn.disabled = false;
    ingestWebsiteBtn.textContent = "Ingest Website";
  }
};

refreshSourcesBtn.onclick = loadSources;

/* 🚫 Prevent accidental form submits */
document.addEventListener("keydown", e => {
  if (e.key === "Enter") e.preventDefault();
});
