console.log("Script gerarnovoalvo.js carregado!");

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;

// Inicializa o canvas com fundo branco
function initCanvas() {
  ctx.fillStyle = 'white';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}
initCanvas();

canvas.addEventListener('mousedown', e => {
  drawing = true;
  ctx.beginPath();
  ctx.moveTo(e.offsetX, e.offsetY);
});

canvas.addEventListener('mousemove', e => {
  if (drawing) {
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.strokeStyle = "#000000";
    ctx.lineWidth = 10;
    ctx.lineCap = "round";
    ctx.stroke();
  }
});

canvas.addEventListener('mouseup', () => {
  drawing = false;
});

canvas.addEventListener('mouseleave', () => {
  drawing = false;
});

function clearCanvas() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  initCanvas();  // pinta o fundo branco novamente
}

let numeroAlvo = gerarNovoAlvo();

function gerarNovoAlvo() {
  const novoNumero = Math.floor(Math.random() * 10);
  document.getElementById("numeroAlvoValor").innerText = novoNumero;
  return novoNumero;
}

function reconhecerDesenho() {
  const resultado = document.getElementById('resultado');
  const acertoSom = document.getElementById('acertoSom');
  const erroSom = document.getElementById('erroSom');

  canvas.toBlob(function(blob) {
    const formData = new FormData();
    formData.append('image', blob, 'desenho.png');

    fetch('/upload', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      resultado.innerText = `Você desenhou: ${data.predicao}`;

      // Função que fala o texto após efeito sonoro com delay
      function falarDepoisDoSom(texto, callback) {
        window.speechSynthesis.cancel(); // Cancela fala pendente
        setTimeout(() => {
          const msg = new SpeechSynthesisUtterance(texto);
          msg.lang = 'pt-BR';
          msg.onend = callback; // chama callback quando termina de falar
          window.speechSynthesis.speak(msg);
        }, 300); // Delay de 300ms antes de falar
      }

      if (data.predicao == numeroAlvo) {
        resultado.style.color = 'green';
        acertoSom.currentTime = 0;

        acertoSom.onended = () => {
          falarDepoisDoSom("Muito bem! Você acertou o número " + data.predicao, () => {
            location.reload(); // Recarrega página após fala
          });
        };
        acertoSom.play();
      } else {
        resultado.style.color = 'red';
        erroSom.currentTime = 0;

        erroSom.onended = () => {
          falarDepoisDoSom("que pena... tente de novo. Eu li " + data.predicao, () => {
            location.reload(); // Recarrega página após fala
          });
        };
        erroSom.play();
      }

      clearCanvas();
    })
    .catch(error => {
      resultado.innerText = "Erro ao reconhecer o desenho.";
      resultado.style.color = 'red';
      console.error("Erro no fetch:", error);
    });
  }, 'image/png');
}
