<template>
  <div v-if="enabled" class="black-gold-ambient" aria-hidden="true">
    <span
      v-for="item in sparks"
      :key="`spark-${item.id}`"
      class="spark"
      :style="{
        left: item.left + '%',
        top: item.top + '%',
        animationDelay: item.delay + 's',
        animationDuration: item.duration + 's',
        transform: `scale(${item.scale})`
      }"
    />
    <span
      v-for="item in ingots"
      :key="`ingot-${item.id}`"
      class="ingot"
      :style="{
        left: item.left + '%',
        top: item.top + '%',
        width: item.width + 'px',
        height: item.height + 'px',
        animationDelay: item.delay + 's',
        animationDuration: item.duration + 's'
      }"
    />
  </div>
</template>

<script>
export default {
  name: 'BlackGoldAmbient',
  data() {
    return {
      ingots: [],
      sparks: []
    }
  },
  computed: {
    enabled() {
      return this.$store.state.app.darkMode
    }
  },
  watch: {
    enabled(val) {
      if (val && (!this.ingots.length || !this.sparks.length)) {
        this.buildParticles()
      }
    }
  },
  mounted() {
    this.buildParticles()
  },
  methods: {
    buildParticles() {
      const rand = (min, max) => Math.random() * (max - min) + min
      const ingots = []
      const sparks = []

      for (let i = 0; i < 7; i++) {
        ingots.push({
          id: i + 1,
          left: rand(1, 99),
          top: rand(2, 98),
          delay: rand(0, 6.2).toFixed(2),
          duration: rand(4.8, 7.6).toFixed(2),
          width: rand(16, 30).toFixed(1),
          height: rand(9, 16).toFixed(1)
        })
      }

      for (let i = 0; i < 20; i++) {
        sparks.push({
          id: i + 1,
          left: rand(1, 99),
          top: rand(4, 98),
          delay: rand(0, 4.5).toFixed(2),
          duration: rand(2.6, 4.8).toFixed(2),
          scale: rand(0.75, 1.45).toFixed(2)
        })
      }

      this.ingots = ingots
      this.sparks = sparks
    }
  }
}
</script>

<style lang="scss" scoped>
.black-gold-ambient {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 8;
}

.ingot {
  position: absolute;
  border-radius: 0 0 10px 10px;
  background: linear-gradient(180deg, rgba(255, 225, 152, 0.96) 0%, rgba(227, 179, 84, 0.96) 58%, rgba(181, 129, 49, 0.96) 100%);
  box-shadow:
    0 0 16px rgba(221, 176, 87, 0.62),
    inset 0 1px 0 rgba(255, 243, 205, 0.68);
  opacity: 0;
  transform: translateY(4px) scale(0.9);
  animation: ingotBlink 6.4s ease-in-out infinite, ingotDrift 5.8s ease-in-out infinite;
  mix-blend-mode: screen;
}

.ingot::before,
.ingot::after {
  content: '';
  position: absolute;
  top: -3px;
  width: 7px;
  height: 8px;
  border-radius: 8px 8px 4px 4px;
  background: linear-gradient(180deg, rgba(255, 235, 176, 0.95) 0%, rgba(219, 168, 74, 0.95) 100%);
}

.ingot::before {
  left: -3px;
  transform: rotate(-18deg);
}

.ingot::after {
  right: -3px;
  transform: rotate(18deg);
}

.spark {
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 239, 188, 0.95) 0%, rgba(230, 186, 94, 0.8) 60%, rgba(0, 0, 0, 0) 100%);
  box-shadow: 0 0 10px rgba(237, 196, 110, 0.5);
  opacity: 0;
  animation: sparkBlink 3.8s ease-in-out infinite;
}

@keyframes ingotBlink {
  0% {
    opacity: 0;
    transform: translateY(4px) scale(0.88);
  }
  22% {
    opacity: 0.52;
    transform: translateY(0) scale(1);
  }
  38% {
    opacity: 0.35;
  }
  55% {
    opacity: 0.68;
    transform: translateY(-2px) scale(1.03) rotate(4deg);
  }
  100% {
    opacity: 0;
    transform: translateY(-6px) scale(0.9) rotate(-5deg);
  }
}

@keyframes ingotDrift {
  0% { margin-left: 0; }
  50% { margin-left: 4px; }
  100% { margin-left: 0; }
}

@keyframes sparkBlink {
  0% {
    opacity: 0;
    transform: scale(0.7);
  }
  30% {
    opacity: 0.85;
    transform: scale(1.2);
  }
  55% {
    opacity: 0.45;
    transform: scale(0.95);
  }
  100% {
    opacity: 0;
    transform: scale(0.7);
  }
}
</style>
