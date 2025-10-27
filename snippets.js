
async function* animate(duration) {
    const start = performance.now();
    let elapsed;
    do {
        await new Promise(requestAnimationFrame);
        yield elapsed = Math.min(performance.now() - start, duration);
    } while (elapsed < duration);
}
