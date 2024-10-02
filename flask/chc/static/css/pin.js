const { createApp } = Vue
  // default PIN is 0000
  createApp({
    data() {
      return {
        bgImage: 'https://source.unsplash.com/random/1920x1080/?city,night',
        pinLength: 6,
        pinInput: [],
        error: null
      }
    },
    methods: {
      keydownHandler(event, index) {
        event.stopPropagation();
        event.preventDefault();
        this.error = null;
        if (event.keyCode == 8) {
          this.pinInput[index - 1] = '';
          this.pinInput[index - 2] = '';
          this.$nextTick(() => {
            this.goto(index - 1);
          });
        } 

        if ((event.keyCode >= 48 && event.keyCode <= 57) || (event.keyCode >= 96 && event.keyCode <= 105)) {
          this.pinInput[index - 1] = event.key;
          this.$nextTick(() => {
            this.goto(index + 1);
          });
          if (index === this.pinLength) {
            this.check();
          }
        }

        if (event.keyCode === 39 && index !== pinLength) {
          this.$nextTick(() => {
            goto(index + 1);
          });
        }

        if (event.keyCode === 37 ) {
          this.$nextTick(() => {
            goto(index - 1);
          });
        }
      },
      reset() {
        document.getElementById("pinForm").reset();
        this.pinInput = new Array(this.pinLength).fill('');
      },
      check() {
        const pin = localStorage.getItem('pin') || Array(this.pinLength).fill(0).join("");
        if (this.pinInput.join("") === "999999") {
          // console.log("Correct!");
          // 设置cookie
          document.cookie = "session=jinhao";
          // sessionStorage.setItem("logged_in", true);
          // sessionStorage.setItem("key", "value");
          // document.cookie = "jinhao"
          window.location.href = "/index";


        } else {
          console.log("err!");
          this.error = "Wrong PIN number!";
        }
        this.reset();
      },
      goto(n) {
        if (!n || n > this.pinLength) {
          n = 1;
        }
        let el = document.querySelector(`input[name=pin${n}]`);
        el.focus();
      }
    },
    mounted() {
      setInterval(() => {
        // Add a unique query parameter to the image URL
        this.bgImage = `https://source.unsplash.com/random/1920x1080/?city,night&t=${Date.now()}`;
      }, 60000);
    }
  }).mount('#app')