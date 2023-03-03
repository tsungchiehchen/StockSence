import { defineStore } from 'pinia'
import axios from "axios"
import { isEmpty } from 'lodash';
import { server } from '../helper';

import { Point, ComponentSize, Margin } from '../types';
interface ScatterPoint extends Point{
    cluster: string;
}

export const useExampleStore = defineStore('exampleWithInteractions', {
    state: () => ({
        points: [] as ScatterPoint[],
        clusters: [] as string[],
        size: { width: 0, height: 0 } as ComponentSize,
        margin: { left: 20, right: 20, top: 20, bottom: 40 } as Margin,
        methods: ['PCA', 't-SNE'] as string[],
        selectedMethod: 'PCA', // default value
    }),
    getters: {
        resize: (state) => {
            return (!isEmpty(state.points) && state.size)
        }
    },
    actions: {
        async fetchExample(method: string) { // same API request but in slightly different syntax when it's declared as a method in a component or an action in the store.
            axios.post(`${server}/fetchExample`, {method: method})
                .then(resp => {
                    this.points = resp.data.data;
                    this.clusters = resp.data.clusters;
                    return true;
                })
                .catch(error => console.log(error));
        },
    }
})