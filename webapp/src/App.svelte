<script lang="ts">
  import Table from '././lib/Table.svelte'
</script>

<main>
  <h1>Osensa Technical Assessment</h1>
  <div class="table-grid">
    <Table tableNum={1} />
    <Table tableNum={2} />
    <Table tableNum={3} />
    <Table tableNum={4} />
  </div>
</main>

<style>
  .table-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-gap: 1rem;
  }
</style>
