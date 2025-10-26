
async function* animate(duration) {
    let progress;
    const start = performance.now();
    do {
        yield progress = Math.min((performance.now() - start) / duration, 1.0);
        await new Promise(requestAnimationFrame);
    } while (progress < 1.0);
}

