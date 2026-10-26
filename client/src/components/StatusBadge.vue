<script setup lang="ts">
import {label} from '../stores/desk'
defineProps<{value:string}>()
</script>
<template><span class="badge" :class="value">{{label(value)}}</span></template>
