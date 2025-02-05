<template>
  <div @drop="drop" @dragover.prevent>
    <h2>Grilla de Datos</h2>
    <table v-if="datos.length > 0">
      <thead>
        <tr>
          <!-- Renderiza los encabezados de la tabla -->
          <th v-for="campo in camposSeleccionados" :key="campo">
            {{ campo }}
          </th>
        </tr>
      </thead>
      <tbody>
        <!-- Renderiza las filas de la tabla -->
        <tr v-for="(fila, index) in datos" :key="index">
          <td v-for="campo in camposSeleccionados" :key="campo">
            {{ fila[campo] }}
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else>No hay datos disponibles</p>
  </div>
</template>

<script>
export default {
  props: ["camposSeleccionados"],
  data() {
    return {
      datos: [], // Almacena los datos de la tabla seleccionada
      tablaSeleccionada: "", // Almacena la tabla seleccionada
    };
  },
  watch: {
    tablaSeleccionada: {
      async handler(newTabla) {
        if (newTabla) {
          try {
            // Obtiene los datos de la tabla seleccionada
            const response = await fetch(`http://localhost:8000/datos/${newTabla}`);
            this.datos = await response.json();
            console.log("Datos obtenidos:", this.datos); // Verifica los datos en la consola
          } catch (error) {
            console.error("Error al obtener datos:", error);
          }
        }
      },
      immediate: true, // Ejecuta la lógica cuando se monta el componente
    },
  },
  methods: {
    drop(event) {
      try {
        const rawData = event.dataTransfer.getData("text/plain");
        console.log("Datos arrastrados:", rawData); // Verifica los datos arrastrados

        const data = JSON.parse(rawData); // Convierte el texto a un objeto JSON
        console.log("Datos recibidos:", data); // Muestra los datos recibidos en consola

        // Si los datos son válidos, actualiza la tabla seleccionada
        if (data && data.tabla) {
          this.tablaSeleccionada = data.tabla; // Establece la tabla seleccionada
          this.cargarDatos(); // Carga los datos de la tabla
          this.camposSeleccionados = data.campos; // Actualiza los campos seleccionados
        }
      } catch (error) {
        console.error("Error al procesar el drop:", error);
      }
    },

    // Método para cargar los datos de la tabla seleccionada
    async cargarDatos() {
      if (this.tablaSeleccionada) {
        try {
          const response = await fetch(`http://localhost:8000/datos/${this.tablaSeleccionada}`);
          const datosObtenidos = await response.json();
          this.datos = datosObtenidos;
          console.log("Datos obtenidos:", this.datos); // Verifica los datos en la consola
        } catch (error) {
          console.error("Error al obtener datos:", error);
        }
      }
    },
  },
};
</script>
