// frontend/src/js/store.js
import { reactive, watch } from 'vue';

export const store = reactive({
    username: localStorage.getItem('username') || '',
    userId: localStorage.getItem('userId') || '',
    roomId: localStorage.getItem('roomId') || '',
    userToken: localStorage.getItem('userToken') || '',
    token: localStorage.getItem('token') || '',
    linkToken: localStorage.getItem('linkToken') || '',
    correctAnswer: localStorage.getItem('correctAnswer') || '',
    isPainter: localStorage.getItem('isPainter') === 'true' || false,
    isEnd: localStorage.getItem('isEnd') === 'true' || false,
    isDialogOpen: localStorage.getItem('isDialogOpen') === 'true' || false,
    blockChat: localStorage.getItem('blockChat') === 'true' || false,
    beforeunmount: localStorage.getItem('beforeunmount') === 'true' || false,
    progressValue: localStorage.getItem('progressValue') || 0,
    dialogProgressValue: localStorage.getItem('dialogProgressValue') || 0,
    answersCount: localStorage.getItem('answersCount') || 0,
});

// Watch for changes to the username and save to localStorage
watch(() => store.username, (newUsername) => {
    localStorage.setItem('username', newUsername);
});
watch(() => store.userId, (newUserId) => {
    localStorage.setItem('userId', newUserId);
});
watch(() => store.userToken, (newUserToken) => {
    localStorage.setItem('userToken', newUserToken);
});
watch(() => store.roomId, (newRoomId) => {
    localStorage.setItem('roomId', newRoomId);
});
watch(() => store.token, (newToken) => {
    localStorage.setItem('token', newToken);
});
watch(() => store.linkToken, (newLinkToken) => {
    localStorage.setItem('linkToken', newLinkToken);
});
watch(() => store.isPainter, (newPainter) => {
    localStorage.setItem('isPainter', newPainter);
});
watch(() => store.beforeunmount, (newBeforeunmount) => {
    localStorage.setItem('beforeunmount', newBeforeunmount);
});
watch(() => store.correctAnswer, (newcorrectAnswer) => {
    localStorage.setItem('correctAnswer', newcorrectAnswer);
});
watch(() => store.blockChat, (newBlockChat) => {
    localStorage.setItem('blockChat', newBlockChat);
});
watch(() => store.isEnd, (newIsEnd) => {
    localStorage.setItem('isEnd', newIsEnd);
});
watch(() => store.isDialogOpen, (newIsDialogOpen) => {
    localStorage.setItem('isDialogOpen', newIsDialogOpen);
});
watch(() => store.progressValue, (newProgressValue) => {
    localStorage.setItem('progressValue', newProgressValue);
});
watch(() => store.dialogProgressValue, (newDialogProgressValue) => {
    localStorage.setItem('dialogProgressValue', newDialogProgressValue);
});
watch(() => store.answersCount, (newAnswersCount) => {
    localStorage.setItem('answersCount', newAnswersCount);
});

