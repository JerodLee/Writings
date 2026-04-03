const STORAGE_KEY = "novel_studio_v1";

const state = {
  title: "",
  genre: "",
  synopsis: "",
  characters: [],
  plots: [],
  timeline: [],
  chapters: []
};

const els = {
  title: document.getElementById("title"),
  genre: document.getElementById("genre"),
  synopsis: document.getElementById("synopsis"),
  characterList: document.getElementById("characterList"),
  plotList: document.getElementById("plotList"),
  timelineList: document.getElementById("timelineList"),
  chapterList: document.getElementById("chapterList"),
  status: document.getElementById("status")
};

const templates = {
  characters: document.getElementById("characterTemplate"),
  plots: document.getElementById("plotTemplate"),
  timeline: document.getElementById("timelineTemplate"),
  chapters: document.getElementById("chapterTemplate")
};

function setStatus(text) {
  els.status.textContent = text;
}

function save(reason = "저장 완료") {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  setStatus(`${reason} · ${new Date().toLocaleTimeString()}`);
}

let saveTimer;
function scheduleSave(reason = "자동 저장") {
  clearTimeout(saveTimer);
  saveTimer = setTimeout(() => save(reason), 250);
}

function getBlankItem(fields) {
  const blank = {};
  fields.forEach((field) => {
    blank[field] = "";
  });
  return blank;
}

function ensureDefaults() {
  if (!state.characters.length) state.characters.push(getBlankItem(["name", "role", "arc"]));
  if (!state.plots.length) state.plots.push(getBlankItem(["label", "detail"]));
  if (!state.timeline.length) state.timeline.push(getBlankItem(["time", "event"]));
  if (!state.chapters.length) state.chapters.push(getBlankItem(["title", "goal", "paragraphs"]));
}

function load() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    ensureDefaults();
    return;
  }

  try {
    Object.assign(state, JSON.parse(raw));
  } catch (error) {
    console.error("저장된 데이터를 불러오지 못했습니다:", error);
    setStatus("저장 데이터가 손상되어 기본 상태로 시작합니다");
  }

  ensureDefaults();
}

function bindSimpleInputs() {
  ["title", "genre", "synopsis"].forEach((key) => {
    els[key].value = state[key] || "";
    els[key].addEventListener("input", (e) => {
      state[key] = e.target.value;
      scheduleSave();
    });
  });
}

function renderCollection(key, container, fields) {
  container.innerHTML = "";

  state[key].forEach((item, index) => {
    const node = templates[key].content.firstElementChild.cloneNode(true);

    fields.forEach((field) => {
      const input = node.querySelector(`[data-field="${field}"]`);
      input.value = item[field] || "";
      input.addEventListener("input", (e) => {
        state[key][index][field] = e.target.value;
        scheduleSave();
      });
    });

    node.querySelector("[data-remove]").addEventListener("click", () => {
      state[key].splice(index, 1);
      if (state[key].length === 0) state[key].push(getBlankItem(fields));
      renderAll();
      save("항목 삭제 저장");
    });

    container.appendChild(node);
  });
}

function renderAll() {
  renderCollection("characters", els.characterList, ["name", "role", "arc"]);
  renderCollection("plots", els.plotList, ["label", "detail"]);
  renderCollection("timeline", els.timelineList, ["time", "event"]);
  renderCollection("chapters", els.chapterList, ["title", "goal", "paragraphs"]);
}

function addItem(key, fields) {
  state[key].push(getBlankItem(fields));
  renderAll();
  save("항목 추가 저장");
}

document.getElementById("addCharacter").addEventListener("click", () => {
  addItem("characters", ["name", "role", "arc"]);
});

document.getElementById("addPlot").addEventListener("click", () => {
  addItem("plots", ["label", "detail"]);
});

document.getElementById("addTimeline").addEventListener("click", () => {
  addItem("timeline", ["time", "event"]);
});

document.getElementById("addChapter").addEventListener("click", () => {
  addItem("chapters", ["title", "goal", "paragraphs"]);
});

document.getElementById("saveBtn").addEventListener("click", () => save("수동 저장"));

document.getElementById("exportBtn").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify(state, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${state.title || "novel-plan"}.json`;
  link.click();
  URL.revokeObjectURL(url);
  setStatus("JSON 내보내기 완료");
});

document.getElementById("resetBtn").addEventListener("click", () => {
  localStorage.removeItem(STORAGE_KEY);
  location.reload();
});

document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "s") {
    e.preventDefault();
    save("단축키 저장");
  }
});

window.addEventListener("beforeunload", () => save("종료 전 저장"));

load();
bindSimpleInputs();
renderAll();
setStatus("실행 준비 완료 · 입력 시 자동 저장됩니다");
