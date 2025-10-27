
async function* animate(duration) {
    const start = performance.now();
    let elapsed;
    do {
        await new Promise(requestAnimationFrame);
        yield elapsed = Math.min(performance.now() - start, duration);
    } while (elapsed < duration);
}

function linear(progress) {
    return progress;
}

function createEasing({from, to, duration, ease = linear}) {
    return function easing(timestamp) {
        progress = ease(timestamp / duration);
        return progress * (to - from) + from;
    }
}
