window.onload = function() {

  const file = document.getElementById("file-input");
  const canvas = document.getElementById("canvas");
  const h3 = document.getElementById('name');
  const audio = document.getElementById("audio");

  file.onchange = function() {

    const files = this.files; // FileList containing File objects selected by the user (DOM File API)
    console.log('FILES[0]: ', files[0]);
    audio.src = URL.createObjectURL(files[0]); // Creates a DOMString containing the specified File object

    const name = files[0].name;
    h3.innerText = `${name}`; // Sets <h3> to the name of the file

    ///////// <CANVAS> INITIALIZATION //////////
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight-200;
    const ctx = canvas.getContext("2d");
    ///////////////////////////////////////////


    const context = new AudioContext(); // (Interface) Audio-processing graph
    let src = context.createMediaElementSource(audio); // Give the audio context an audio source,
    // to which can then be played and manipulated
    const analyser = context.createAnalyser(); // Create an analyser for the audio context

    src.connect(analyser); // Connects the audio context source to the analyser
    analyser.connect(context.destination); // End destination of an audio graph in a given context
    // Sends sound to the speakers or headphones


    /////////////// ANALYSER FFTSIZE ////////////////////////
    // analyser.fftSize = 32;
    // analyser.fftSize = 64;
    // analyser.fftSize = 128;
    // analyser.fftSize = 256;
    // analyser.fftSize = 512;
    // analyser.fftSize = 1024;
    // analyser.fftSize = 2048;
    // analyser.fftSize = 4096;
    // analyser.fftSize = 8192;
    analyser.fftSize = 16384;
    // analyser.fftSize = 32768;

    // (FFT) is an algorithm that samples a signal over a period of time
    // and divides it into its frequency components (single sinusoidal oscillations).
    // It separates the mixed signals and shows what frequency is a violent vibration.

    // (FFTSize) represents the window size in samples that is used when performing a FFT

    // Lower the size, the less bars (but wider in size)
    ///////////////////////////////////////////////////////////


    const bufferLength = analyser.frequencyBinCount; // (read-only property)
    // Unsigned integer, half of fftSize (so in this case, bufferLength = 8192)
    // Equates to number of data values you have to play with for the visualization

    // The FFT size defines the number of bins used for dividing the window into equal strips, or bins.
    // Hence, a bin is a spectrum sample, and defines the frequency resolution of the window.

    const dataArray = new Uint8Array(bufferLength); // Converts to 8-bit unsigned integer array
    // At this point dataArray is an array with length of bufferLength but no values
    console.log('DATA-ARRAY: ', dataArray) // Check out this array of frequency values!

    const WIDTH = canvas.width;
    const HEIGHT = canvas.height;
    console.log('WIDTH: ', WIDTH, 'HEIGHT: ', HEIGHT)

    const barWidth = (WIDTH / bufferLength) * 13;
    console.log('BARWIDTH: ', barWidth)

    console.log('TOTAL WIDTH: ', (117*10)+(118*barWidth)) // (total space between bars)+(total width of all bars)

    let barHeight;
    let x = 0;

    function renderFrame() {
      requestAnimationFrame(renderFrame); // Takes callback function to invoke before rendering

      x = 0;

      analyser.getByteFrequencyData(dataArray); // Copies the frequency data into dataArray
      // Results in a normalized array of values between 0 and 255
      // Before this step, dataArray's values are all zeros (but with length of 8192)

      ctx.fillStyle = "rgba(0,0,0,0.2)"; // Clears canvas before rendering bars (black with opacity 0.2)
      ctx.fillRect(0, 0, WIDTH, HEIGHT); // Fade effect, set opacity to 1 for sharper rendering of bars

      let r, g, b;
      let bars = 118 // Set total number of bars you want per frame

      for (let i = 0; i < bars; i++) {
        barHeight = (dataArray[i] * 2.5);

        if (dataArray[i] > 210){ // pink
          r = 250;
          g = 0;
          b = 255;
        } else if (dataArray[i] > 200){ // yellow
          r = 250;
          g = 255;
          b = 0;
        } else if (dataArray[i] > 190){ // yellow/green
          r = 204;
          g = 255;
          b = 0;
        } else if (dataArray[i] > 180){ // blue/green
          r = 0;
          g = 219;
          b = 131;
        } else { // light blue
          r = 0;
          g = 199;
          b = 255;
        }

        // if (i === 0){
        //   console.log(dataArray[i])
        // }

        ctx.fillStyle = `rgb(${r},${g},${b})`;
        ctx.fillRect(x, (HEIGHT - barHeight), barWidth, barHeight);
        // (x, y, i, j)
        // (x, y) Represents start point
        // (i, j) Represents end point

        x += barWidth + 10; // Gives 10px space between each bar
      }
    }

    audio.play();
    renderFrame();
  };
};


// analyze
const file = document.getElementById("file-input");
      file.addEventListener('change', ()=>{
        const files = this.files; // FileList containing File objects selected by the user (DOM File API)
        let audioPath = URL.createObjectURL(files[0]); // Creates a DOMString containing the specified File object
        console.log(audioPath)
      });

      // Hacks to deal with different function names in different browsers
      window.requestAnimFrame = (function(){
        return  window.requestAnimationFrame       ||
                window.webkitRequestAnimationFrame ||
                window.mozRequestAnimationFrame    ||
                function(callback, element){
                  window.setTimeout(callback, 1000 / 60);
                };
      })();

      window.AudioContext = (function(){
          return  window.webkitAudioContext || window.AudioContext || window.mozAudioContext;
      })();

      // Global Variables for Audio
      var audioContext;
      var audioBuffer;
      var sourceNode;
      var analyserNode;
      var javascriptNode;
      var audioData = null;
      var audioPlaying = false;
      var sampleSize = 1024;  // number of samples to collect before analyzing data
      var amplitudeArray;     // array to hold time domain data

      // This must be hosted on the same server as this page - otherwise you get a Cross Site Scripting error
      var audioUrl = audioPath;

      // Global Variables for the Graphics
      var canvasWidth  = 512;
      var canvasHeight = 256;
      var ctx;

      $(document).ready(function() {

          ctx = $("#canvas1").get()[0].getContext("2d");

          // the AudioContext is the primary 'container' for all your audio node objects
          try {
              audioContext = new AudioContext();
          } catch(e) {
              alert('Web Audio API is not supported in this browser');
          }

          // When the Start button is clicked, finish setting up the audio nodes, play the sound,
          // gather samples for the analysis, update the canvas
              e.preventDefault();

              // Set up the audio Analyser, the Source Buffer and javascriptNode
              setupAudioNodes();

              // setup the event handler that is triggered every time enough samples have been collected
              // trigger the audio analysis and draw the results
              javascriptNode.onaudioprocess = function () {

                  // get the Time Domain data for this sample
                  analyserNode.getByteTimeDomainData(amplitudeArray);

                  // draw the display if the audio is playing
                  if (audioPlaying == true) {
                      requestAnimFrame(drawTimeDomain);
                  }
              }

              // Load the Audio the first time through, otherwise play it from the buffer
              if(audioData == null) {
                  loadSound(audioUrl);
              } else {
                  playSound(audioData);
              }

          // Stop the audio playing

              e.preventDefault();
              sourceNode.stop(0);
              audioPlaying = false;

      });

      function setupAudioNodes() {
          sourceNode     = audioContext.createBufferSource();
          analyserNode   = audioContext.createAnalyser();
          javascriptNode = audioContext.createScriptProcessor(sampleSize, 1, 1);

          // Create the array for the data values
          amplitudeArray = new Uint8Array(analyserNode.frequencyBinCount);

          // Now connect the nodes together
          sourceNode.connect(audioContext.destination);
          sourceNode.connect(analyserNode);
          analyserNode.connect(javascriptNode);
          javascriptNode.connect(audioContext.destination);
      }

      // Load the audio from the URL via Ajax and store it in global variable audioData
      // Note that the audio load is asynchronous
      function loadSound(url) {
          var request = new XMLHttpRequest();
          request.open('GET', url, true);
          request.responseType = 'arraybuffer';

          // When loaded, decode the data and play the sound
          request.onload = function () {
              audioContext.decodeAudioData(request.response, function (buffer) {
                  audioData = buffer;
                  playSound(audioData);
              }, onError);
          }
          request.send();
      }

      // Play the audio and loop until stopped
      function playSound(buffer) {
          sourceNode.buffer = buffer;
          sourceNode.start(0);    // Play the sound now
          sourceNode.loop = true;
          audioPlaying = true;
      }

      function onError(e) {
          console.log(e);
      }

      function drawTimeDomain() {
          clearCanvas();
          for (var i = 0; i < amplitudeArray.length; i++) {
              var value = amplitudeArray[i] / 256;
              var y = canvasHeight - (canvasHeight * value) - 1;
              ctx.fillStyle = '#ffffff';
              ctx.fillRect(i, y, 1, 1);
          }
      }

      function clearCanvas() {
          ctx.clearRect(0, 0, canvasWidth, canvasHeight);
      }