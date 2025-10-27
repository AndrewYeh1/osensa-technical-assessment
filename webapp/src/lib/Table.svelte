<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import mqtt from 'mqtt';
  import type { MqttClient } from 'mqtt';
  import Popup from './Popup.svelte';

  let {
    tableNum = 0
  } = $props <{
    tableNum?: number
  }> ();

  let foodOrder: string = $state("")

  let client: MqttClient;
  let status = $state('Connecting...');

  onMount(() => {
    const url = 'ws://localhost:9001';
    client = mqtt.connect(url);

    client.on('connect', () => {
      status = 'Connected';
      client.subscribe('foodServer');
      console.log(`Table ${tableNum} connected.`);
    });

    client.on('message', (topic, payload) => {
      const response: string = payload.toString();
      const parsedResponse = JSON.parse(response);
      if (parsedResponse.table == tableNum) {
        addFood(parsedResponse.food);
        console.log(`Table ${tableNum} was served food.`);
      }
    });

    client.on('error', () => {
      status = 'Error';
      console.log(`Table ${tableNum} experienced a connection error.`);
    });
  });

  onDestroy(() => {
    if (client) {
      client.end();
      console.log(`Table ${tableNum} disconnected.`);
    }
  });

  const sendOrder = () => {
    if (foodOrder === "") {return}
    const payload: string = JSON.stringify({
      table: tableNum,
      food: foodOrder
    });
    client.publish('foodOrder', payload);
  }

  let foods = $state<string[]>([]);

  function addFood(newFood: string) {
    if (newFood.trim()) {
      foods = [...foods, newFood];
    }
  }

  let isPopupOpen = $state(false);
  const openOrderPopup = () => isPopupOpen = true;
  const closeOrderPopup = () => isPopupOpen = false;
</script>

<main>
  <div class=table>
    <h3>
      Table {tableNum}
    </h3>

    <ul class=food-list>
      {#each foods as food, index (index)}
        <li>{food}</li>
      {/each}
    </ul>

    <button onclick={openOrderPopup}>
      Order
    </button>
  </div>

  <Popup show={isPopupOpen} close={closeOrderPopup}>
    <h4>Ordering for table {tableNum}</h4>
    <input
      type="text"
      bind:value={foodOrder}
      placeholder="Enter item..."
    />
    <button onclick={sendOrder}>
      Order
    </button>
  </Popup>
</main>

<style>
  .table {
    border: 1px solid;
    border-radius: 5px;
    padding: 1rem;
  }

  .food-list {
    padding-left: 0;
    list-style-type: none;
    height: 150px;
    overflow-y: auto;
  }
</style>
