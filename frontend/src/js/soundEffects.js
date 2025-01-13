import hoverSound from "../sound_pack/button_hover.mp3"
import clickSound from "../sound_pack/button_click.mp3"
import drawingSound from "../sound_pack/drawing-sound.mp3"

export function playHoverSound() {
    const audio = new Audio(hoverSound);
    audio.play();
}

export function playClickSound() {
    const audio = new Audio(clickSound);
    audio.play();
}

export function playDrawingSound() {
    const audio = new Audio(drawingSound);
    audio.play();
}