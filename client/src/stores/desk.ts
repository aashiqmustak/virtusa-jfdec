import {reactive} from 'vue'
import type {Case} from '../types'
export const desk=reactive({view:'dashboard',selected:null as Case|null,error:'',busy:false})
export function inr(value:unknown){return value===null||value===undefined?'Insufficient evidence':new Intl.NumberFormat('en-IN',{style:'currency',currency:'INR',maximumFractionDigits:0}).format(Number(value))}
export function label(value:string){return value.replaceAll('_',' ')}
