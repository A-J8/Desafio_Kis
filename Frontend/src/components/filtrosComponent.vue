<template>
  <div @drop="drop" @dragover.prevent>
    <h2>Filtros</h2>
    <p>Arrastra campos aquí para filtrar</p>
    <div v-for="(filtro, index) in filtros" :key="index">
      <label>{{ filtro.campo }}</label>
      <input v-model="filtro.valor" @input="aplicarFiltro" />
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filtros: [],
    };
  },
  methods: {
    drop(event) {
      // Obtener el campo arrastrado
      const data = JSON.parse(event.dataTransfer.getData("text/plain"));
      this.filtros.push({ campo: data.campo, valor: "" });
    },
    aplicarFiltro() {
      // Emitir los filtros al componente padre
      this.$emit("filtro-aplicado", this.filtros);
    },
  },
};
</script>