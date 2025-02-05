<template>
  <v-container>
    <h1 class="text-h3 font-weight-bold text-center mb-6">Desafio Kis</h1>
    <h4 class="text-h6 text-center ">Arrastrar campos a las areas grises</h4>
    <v-row>
      <!-------------  Área de Selección de Tablas y Campos ------------------>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>Selección de Tablas y Campos</v-card-title>
          <v-card-text>
            <v-select
              v-model="selectedTable"
              :items="Object.keys(tablas)"
              label="Seleccionar Tabla"
              outlined
              @change="resetSelections"
            ></v-select>

            <v-list v-if="selectedTable" two-line>
              <v-subheader>Campos:</v-subheader>
              <draggable
                :list="tablas[selectedTable].campos"
                :group="{ name: 'fields', pull: 'clone', put: false }"
                item-key="id"
              >
                <template #item="{ element }">
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-title>{{ element.nombre }}</v-list-item-title>
                      <v-list-item-subtitle>{{ element.tipo }}</v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </template>
              </draggable>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card>
          <v-card-text>
            <!------------------- Área de Filtros --------------------------------->
            <v-sheet class="pa-4 mb-4" color="grey lighten-4" rounded>
              <h4>Área de Filtros:</h4>
              <draggable
                v-model="filterCampos"
                :group="{ name: 'fields', pull: true, put: true }"
                item-key="id"
                @change="updateFilters"
              >
                <template #item="{ element }">
                  <v-chip class="ma-2">
                    <v-btn class="no-background " icon small @click="eliminarCampoFiltro(element)">
                      <v-icon small color="red" >mdi-close-circle-outline</v-icon>
                    </v-btn>
                    {{ element.nombre }}
                    <v-select
                      v-model="filterValues[element.nombre]"
                      :items="getUniqueValues(element.nombre)"
                      
                      chips
                      small-chips
                      deletable-chips
                      class="ml-2"
                      style="min-width: 150px;"
                    ></v-select>
                  </v-chip>
                </template>
              </draggable>

              <v-btn color="primary" @click="applyFilters">Aplicar Filtros</v-btn>
            </v-sheet>

            <!------------------- Área de Visualización de Datos (Grilla de Datos) ---------------->
            <v-sheet class="pa-4 mb-4" color="grey lighten-4" rounded>
              <h4>Campos Seleccionados:</h4>
              <draggable
                v-model="selectedCampos"
                :group="{ name: 'fields', pull: true, put: true }"
                item-key="id"
                @change="fetchFilteredData"
              >
                <template #item="{ element }">
                  <v-chip class="ma-2">
                    <v-btn class="no-background " icon small @click="eliminarCampo(element)">
                      <v-icon small color="red" >mdi-close-circle-outline</v-icon>
                    </v-btn>
                    {{ element.nombre }}
                  </v-chip>
                </template>
              </draggable>
            </v-sheet>
            <v-card-title>Tabla visualizacion</v-card-title>
            <template v-if="selectedCampos.length > 0">
            <v-table height="300px" fixed-header>
              <thead>
                <tr>
                  <th v-for="header in tableHeaders" :key="header.value" class="text-left font-weight-bold">
                    {{ header.text }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in filteredData" :key="index">
                  <td v-for="header in tableHeaders" :key="header.value">
                    {{ item[header.value] }}
                  </td>
                </tr>
              </tbody>
            </v-table>
          </template>
            <v-alert v-else type="info" text>
              Arrastra los campos desde la lista de la izquierda para mostrar la informacion de la columna
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import draggable from 'vuedraggable'

export default {
  name: 'DataVisualization',
  components: {
    draggable
  },
  data() {
    return {
      tablas: {},
      selectedTable: '',
      selectedCampos: [],
      filterCampos: [],
      filterValues: {},
      allData: [],
      filteredData: []
    }
  },
  computed: {
    tableHeaders() {
      return this.selectedCampos.map(campo => ({
        text: campo.nombre,
        value: campo.nombre,
        sortable: true
      }))
    }
  },
  methods: {
    //PARA EL SELECT DE LA IZQUIERDA DONDE SE OBTIENEN CAMPOS
    fetchTables() {
      axios.get('http://localhost:8000/tablas')
        .then(response => {
          this.tablas = response.data.tablas
        })
        .catch(error => {
          console.error('Error al obtener tablas y columnas:', error)
        })
    },

    clearData() {
      this.allData = []
      this.filteredData = []
    },
    //IR MOSTRANDO DATOS EN TABLA SEGUN DATOS SELECCIONADOS
    async fetchFilteredData() {
      if (!this.selectedTable || this.selectedCampos.length === 0) {
        this.clearData()
        return
      }

      try {
        const selectedFields = this.selectedCampos.map(({ nombre }) => nombre)

        const { data } = await axios.post("http://localhost:8000/data", {
          table: this.selectedTable,
          selected_fields: selectedFields
        })

        this.allData = data?.data || []
        this.applyFilters()

      } catch (error) {
        console.error("Error al obtener datos:", error)
        this.clearData()
      }
    },
    getUniqueValues(column) { 
      return [...new Set(this.allData.map(item => item[column]))]
    },
    //APLICAR FILTROS EN TABLA
    applyFilters() {
      this.filteredData = this.allData.filter(item => {
        return this.filterCampos.every(campo => {
          if (!this.filterValues[campo.nombre] || this.filterValues[campo.nombre].length === 0) {
            return true
          }
          return this.filterValues[campo.nombre].includes(item[campo.nombre])
        })
      })
    },
    
    eliminarCampoFiltro(campo) {
      const index = this.filterCampos.indexOf(campo)
      if (index > -1) {
        this.filterCampos.splice(index, 1)
        delete this.filterValues[campo.nombre]
        this.applyFilters()
      }
    },
    eliminarCampo(campo) {
      const index = this.selectedCampos.indexOf(campo)
      if (index > -1) {
        this.selectedCampos.splice(index, 1)
        this.fetchFilteredData()
      }
    },
    resetSelections() {
      this.selectedCampos = []
      this.filterCampos = []
      this.filterValues = {}
      this.clearData()
    },
  },
  mounted() {
    this.fetchTables()
  }
}
</script>

<style scoped>
.v-chip {
  margin-right: 8px;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
}
.no-background {
  background: none !important;
}
</style>

