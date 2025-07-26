<template>
  <s-page>
    <s-header :create-btn="false" title="Перейдите в сайдабар" />
    <div class="home_wrapper">
     
    </div>
  </s-page>
</template>

<script>
import { ref, onMounted } from 'vue';
import 'webrtc-adapter';

export default {
  setup() {
    const peerConnection = ref(new RTCPeerConnection());
    const localStream = ref(null);

    const clientID = ref(generateID())
    const remoteClientID = ref('')

    const user1Video = ref(null);
    const user2Video = ref(null);
    const ws = ref(null)

    onMounted(() => {
      ws.value = new WebSocket(`ws://127.0.0.1:8007/ws/test/${clientID.value}`);

      ws.value.onopen = () => {
        console.log('WebSocket connected');
      };

      ws.value.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('Received from server:', data);
        // Обрабатываем сообщения от сервера
        if (data.sdp && data.type === 'offer') {
          console.log('Получен offer', data.sdp)
          createAnswer(data.sdp)
        } else if (data.sdp && data.type === 'answer') {
          console.log('Получен answer', data.sdp)
          addAnswer(data.sdp)
        }
        else if (data.error) {
          console.error('Error from server:', data.error);
          alert(data.error)
        }
        else if (data.candidate) {
            console.log('Received ICE candidate:', data.candidate);
            peerConnection.value.addIceCandidate(data.candidate)
                .catch(e => console.error('Error adding ice candidate', e));
        }
      };

      ws.value.onclose = () => {
        console.log('WebSocket disconnected');
      };

      ws.value.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    });

      const sendOffer = (offer, to) => {
      if (ws.value && ws.value.readyState === WebSocket.OPEN) {
        ws.value.send(JSON.stringify({ type: 'offer', sdp: offer, to:to }));
        console.log('Отправлен offer')
      } else {
        console.error('WebSocket not connected');
        alert('WebSocket not connected')
      }
    };

        const sendAnswer = (answer, to) => {
      if (ws.value && ws.value.readyState === WebSocket.OPEN) {
        ws.value.send(JSON.stringify({ type: 'answer', sdp: answer, to:to }));
        console.log('Отправлен answer')
      } else {
        console.error('WebSocket not connected');
        alert('WebSocket not connected')
      }
    };

     const sendIceCandidate = (candidate, to) => {
        if (ws.value && ws.value.readyState === WebSocket.OPEN) {
            ws.value.send(JSON.stringify({ type: 'iceCandidate', candidate: candidate, to: to }));
            console.log('Отправлен ICE candidate');
        } else {
            console.error('WebSocket not connected');
            alert('WebSocket not connected');
        }
    };

    const init = async () => {
        try {
            localStream.value = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
            user1Video.value.srcObject = localStream.value;

            localStream.value.getTracks().forEach((track) => {
                peerConnection.value.addTrack(track, localStream.value);
            });

            peerConnection.value.ontrack = (event) => {
                console.log('Received remote stream');
                const remoteStream = event.streams[0];  // Получаем MediaStream из события
                user2Video.value.srcObject = remoteStream; // Привязываем поток к video элементу
            };

             peerConnection.value.onicecandidate = (event) => {
                if (event.candidate) {
                    console.log('New ICE candidate:', event.candidate);
                    // Send ICE candidate to the remote peer through the signaling server
                    sendIceCandidate(event.candidate, remoteClientID.value);
                }
            };
        } catch (error) {
            console.error('Error initializing WebRTC:', error);
        }
    };

     const createOffer = async () => {
        try {
            await init()
            const offer = await peerConnection.value.createOffer();
            await peerConnection.value.setLocalDescription(offer);
            console.log('Offer created:', offer);
            sendOffer(offer.sdp, remoteClientID.value);
        } catch (error) {
            console.error('Error creating offer:', error);
        }
    };

    const createAnswer = async (offer) => {
        try {
             await init()
            const offerDescription = {
                type: 'offer',
                sdp: offer,
            };

            await peerConnection.value.setRemoteDescription(offerDescription);
            const answer = await peerConnection.value.createAnswer();
            await peerConnection.value.setLocalDescription(answer);
            console.log('Answer created:', answer);

            sendAnswer(answer.sdp, remoteClientID.value);
        } catch (error) {
            console.error('Error creating answer:', error);
        }
    };

        const addAnswer = async (answer) => {
        try {

            const answerDescription = {
                type: 'answer',
                sdp: answer,
            };

            await peerConnection.value.setRemoteDescription(answerDescription);
            console.log('Answer added.');
        } catch (error) {
            console.error('Error adding answer:', error);
        }
    };

    function generateID() {
        return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    }


    return {
      clientID,
      remoteClientID,
      user1Video,
      user2Video,
      createOffer,
      createAnswer,
      addAnswer,
      sendIceCandidate
    };
  },
};
</script>

<style scoped>
.home_wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.home_wrapper video {
    width: 320px;
    height: 240px;
    border: 1px solid black;
    margin-bottom: 10px;
}

.step {
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: 80%;
    text-align: center;
}

.step p {
    margin-bottom: 10px;
}

.step button {
    padding: 8px 16px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

input[type="text"] {
    width: 80%;
    padding: 8px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
}
</style>