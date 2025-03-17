<template v-if="props.hashStr">
    
    <div class="home_wrapper">
      <video ref="localVideo" autoplay muted></video>
      <video ref="remoteVideo" autoplay></video>
     </div>

    <div class="home_wrapper">

    </div>
    
</template>
<script>
import { ref, onMounted } from 'vue';

export default {
  props : {
      hashStr: String
  },
  
  setup(props) {
    const localVideo = ref(null);
    const remoteVideo = ref(null);
    // const roomHash = location.hash ? location.hash.substring(1) : '1234567';
    const roomHash = props.hashStr;
    const roomName = 'observable-' + roomHash;
  
    const drone = new ScaleDrone('0QuRggLzh0KMzqc7');
    const configuration = {
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    };
    let room;
    let pc;

    // eslint-disable-next-line @typescript-eslint/no-empty-function
    const onSuccess = () => {};
    const onError = (error) => {
      console.error(error);
    };

    const sendMessage = (message) => {
      drone.publish({
        room: roomName,
        message
      });
    };

    const localDescCreated = (desc) => {
      pc.setLocalDescription(
        desc,
        () => sendMessage({ 'sdp': pc.localDescription }),
        onError
      );
    };

    const startWebRTC = (isOfferer) => {
      pc = new RTCPeerConnection(configuration);

      pc.onicecandidate = (event) => {
        if (event.candidate) {
          sendMessage({ 'candidate': event.candidate });
        }
      };

      if (isOfferer) {
        pc.onnegotiationneeded = () => {
          pc.createOffer().then(localDescCreated).catch(onError);
        };
      }

      pc.ontrack = (event) => {
        const stream = event.streams[0];
        if (!remoteVideo.value.srcObject || remoteVideo.value.srcObject.id !== stream.id) {
          remoteVideo.value.srcObject = stream;
        }
      };

      navigator.mediaDevices.getUserMedia({ audio: true, video: true })
        .then((stream) => {
          localVideo.value.srcObject = stream;
          stream.getTracks().forEach((track) => pc.addTrack(track, stream));
        })
        .catch(onError);

      room.on('data', (message, client) => {
        if (client.id === drone.clientId) {
          return;
        }

        if (message.sdp) {
          pc.setRemoteDescription(new RTCSessionDescription(message.sdp), () => {
            if (pc.remoteDescription.type === 'offer') {
              pc.createAnswer().then(localDescCreated).catch(onError);
            }
          }, onError);
        } else if (message.candidate) {
          pc.addIceCandidate(new RTCIceCandidate(message.candidate), onSuccess, onError);
        }
      });
    };

    onMounted(() => {
      drone.on('open', (error) => {
        if (error) {
          return console.error(error);
        }
        room = drone.subscribe(roomName);
        room.on('open', (error) => {
          if (error) {
            onError(error);
          }
        });

        room.on('members', (members) => {
          console.log('MEMBERS', members);
          const isOfferer = members.length === 2;
          startWebRTC(isOfferer);
        });
      });
    });

    return {
      localVideo,
      remoteVideo
    };
  }
};
</script>
<style>
.container {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  position: relative;
}

.row-my {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.details-block {
  background: #423e3e;
  padding: 1rem;
  margin-top: 1rem;
  position: absolute;
  top: 100px;
  /* bottom: 50px; */
  left: 0;
  width: 100%;
  z-index: 10; /* Чтобы блок был над карточками */
}
</style>
<style>
/* Добавьте стили для ваших видео элементов, если необходимо */
video {
  width: 100%;
  max-width: 600px;
}
</style>