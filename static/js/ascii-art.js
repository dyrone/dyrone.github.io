// Draws the ASCII scenes in static/js/ascii-art/ onto their canvases. A scene
// returns one frame of text per call and fills a palette index per cell.
(() => {
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function start(canvas) {
    const scene = (window.asciiArtScenes || {})[canvas.dataset.asciiPiece];
    if (!scene) return;
    const { meta } = scene;
    const context = canvas.getContext("2d", { alpha: false });
    const cellWidth = canvas.width / meta.cols;
    const cellHeight = canvas.height / meta.rows;
    const frameInterval = 1000 / meta.fps;
    const colors = new Uint8Array(meta.cols * meta.rows);
    let render = null;
    let startedAt = 0;
    let lastFrameAt = 0;
    let visible = false;
    let frameCount = 0;

    function draw(seconds) {
      const lines = render(seconds, { color: colors }).split("\n");
      context.fillStyle = meta.ground;
      context.fillRect(0, 0, canvas.width, canvas.height);
      context.font = `${cellHeight}px ui-monospace, SFMono-Regular, Menlo, Consolas, monospace`;
      context.textBaseline = "bottom";
      let index = 0;
      for (let row = 0; row < meta.rows; row++) {
        const line = lines[row] || "";
        for (let column = 0; column < meta.cols; column++, index++) {
          const character = line[column];
          if (!character || character === " ") continue;
          context.fillStyle = meta.palette[colors[index]] || meta.palette[0];
          context.fillText(character, column * cellWidth, (row + 1) * cellHeight);
        }
      }
      canvas.dataset.frameCount = String(++frameCount);
      if (frameCount === 1) canvas.closest("figure").classList.add("ready");
    }

    function tick(now) {
      if (!visible) return;
      requestAnimationFrame(tick);
      if (now - lastFrameAt < frameInterval) return;
      lastFrameAt = now;
      draw((now - startedAt) / 1000);
    }

    // Pause while scrolled out of view; build the scene on first sight,
    // since its one-off raymarch takes a few hundred milliseconds.
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      if (!visible) return;
      if (!render) {
        render = scene.create();
        startedAt = performance.now();
      }
      if (reduceMotion) {
        if (!frameCount) draw(0);
        return;
      }
      requestAnimationFrame(tick);
    }).observe(canvas);
  }

  document.querySelectorAll("canvas[data-ascii-piece]").forEach(start);
})();
