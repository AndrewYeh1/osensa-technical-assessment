<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import mqtt from 'mqtt';
  import type { MqttClient } from 'mqtt';

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
    });

    client.on('message', (topic, payload) => {
      let foodServe: string = payload.toString();
      addFood(foodServe);
    });

    client.on('error', () => {
      status = 'Error';
    });
  });

  onDestroy(() => {
    if (client) {
      client.end();
    }
  });

  const sendOrder = () => {
    client.publish('foodOrder', foodOrder);
  }

  let foods = $state<string[]>([]);

  function addFood(newFood: string) {
    if (newFood.trim()) {
      foods = [...foods, newFood];
    }
  }
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

    <input
      id="single"
      type="text"
      bind:value={foodOrder}
      placeholder="Make an order..."
    />
    <button onclick={sendOrder}>
      Order
    </button>
  </div>
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
  }
</style>
