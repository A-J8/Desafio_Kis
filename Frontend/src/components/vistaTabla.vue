<template>
  <div>
    <h2>Tablas Disponibles</h2>
    <ul>
      <li v-for="(campos, tabla) in tablas" :key="tabla">
        <strong>{{ tabla }}</strong>
        <ul>
          <li
            v-for="campo in campos"
            :key="campo"
            draggable="true"
            @dragstart="dragStart($event, tabla, campo)"
          >
            {{ campo }}
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tablas: {},
    };
  },
  async created() {
    const response = await fetch("http://localhost:8000/tablas");
    this.tablas = await response.json();
  },
  methods: {
    dragStart(event, tabla, campo) {
      const data = { tabla, campo }; // Crear un objeto con la tabla y el campo
      const jsonData = JSON.stringify(data); // Convertir a JSON
      console.log("Datos arrastrados:", jsonData); // Verifica en la consola
      event.dataTransfer.setData("text/plain", jsonData); // Pasar el JSON como texto
    },
  },
};
</script>