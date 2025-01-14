import hoverSound from "../sound_pack/button_hover.mp3";
import clickSound from "../sound_pack/button_click.mp3";
import choosingWordSound from "../sound_pack/choosing_word_sound.mp3";
import correctAnswerSound from "../sound_pack/correct_answer_sound.mp3";
import timerSound from "../sound_pack/timer_sound.mp3";
import warningSound from "../sound_pack/warning_sound.mp3";
import gameMusic from "../sound_pack/game_music.mp3"

let timerAudio = null;
let soundsEnabled = true;
let currentPlayingSounds = [];

export function toggleSounds() {
    soundsEnabled = !soundsEnabled;
    currentPlayingSounds.forEach(audio => {
        if (audio === timerAudio) {
            audio.volume = soundsEnabled ? 0.1 : 0;
        } else if (audio.src.includes(gameMusic)){
            audio.volume = soundsEnabled ? 0.05 : 0;
        }
        else {
            audio.volume = soundsEnabled ? 1 : 0;
        }
    });
}

function playSound(audio, volume = 1) {
    audio.volume = soundsEnabled ? volume : 0;
    audio.play();
    currentPlayingSounds.push(audio);
}

export function playHoverSound() {
    const audio = new Audio(hoverSound);
    playSound(audio);
}

export function playClickSound() {
    const audio = new Audio(clickSound);
    playSound(audio);
}

export function playChoosingWordSound() {
    const audio = new Audio(choosingWordSound);
    playSound(audio);
}

export function playCorrectAnswerSound() {
    const audio = new Audio(correctAnswerSound);
    playSound(audio);
}

export function playTimerSound() {
    if (!timerAudio) {
        timerAudio = new Audio(timerSound);
        timerAudio.loop = true;
    }
    timerAudio.volume = soundsEnabled ? 0.1 : 0;
    playSound(timerAudio, 0.1);
}

export function playStopTimerSound() {
    if (timerAudio) {
        timerAudio.pause();
        timerAudio.currentTime = 0;
        currentPlayingSounds = currentPlayingSounds.filter(audio => audio !== timerAudio);
    }
}

export function playWarningSound() {
    const audio = new Audio(warningSound);
    playSound(audio);
}

export function playGameMusic() {
    const audio = new Audio(gameMusic);
    audio.loop = true;
    playSound(audio, 0.05);
}
export function stopGameMusic() {
    currentPlayingSounds.forEach(audio => {
        if (audio.src.includes(gameMusic)) {
            audio.pause();
            audio.currentTime = 0;
            currentPlayingSounds = currentPlayingSounds.filter(a => a !== audio);
        }
    });
}