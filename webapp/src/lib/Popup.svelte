<script lang="ts">
  import type { Snippet } from 'svelte';

  let {
    show = false,
    close,
    children
  } = $props<{
    show?: boolean,
    close: () => void
    children: Snippet
  }>();
</script>

{#if show}
  <div class="popup">
    <button class="close-button" onclick={close}>x</button>
    {@render children()}
  </div>
{/if}

<style>
  .popup {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: rgb(133, 133, 133);
    padding: 2rem;
    border-radius: 8px;
    z-index: 11;
    min-width: 300px;
  }

  .close-button {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #555;
  }
</style>