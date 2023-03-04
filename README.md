# More about the Framework

This is a tempalate in Vue.js. Vue 3.0 sits between React and basic JavaScript depending on the developers comfort level. For this class, we stick with [Options API](https://vuejs.org/api/#options-api) rather than Composition API (not required so you can switch depending on how you feel). We offer Vue, since it is a modern framework that companies use so it could be useful for you if one of your projects in this class could make use of it.

What this page covers:
 - Pointers if you want to use your own setup or a simpler template for the assignment
 - **The files you have to care about**
 - Libraries used in this framework
 - Some pointers that help you pick up D3.js
 - What the three demo examples are doing

## Setting up a Different Template

If you want to use React or vanilla JavaScript/TypeScript instead of Vue, you can follow [here on Vite](https://vitejs.dev/guide/#trying-vite-online) to create your template. <br />

In general, `./dashboard/package.json` is how the dashboard and the server set up together. This is probably the only technical thing you need to know for customizing your web-based application.

## The Files You Have to Care about

### `./server` 
 * `app.py` tends to be where you manage only the API requests. <br />
 * `controller.py` would be where the data analysis being performed on demand.

### `./dashboard`
* Most of the files you can ignore, but **the files under `./src/` are your concern**.
* `./src/main.ts` is the root script file for Vue.js that instatinates our single page application.
* `./src/App.vue` is the root file for all **development** needs and is also where we manage the layout and load in components.
* `./src/types.ts` is usually where we declare our customized types (if you have any)
* `./src/stores/` is where we manage the stores if you're planning to use it. The store is a container that holds your application state.
* `./src/components/` is where we create the components. You may have multiple components depends on your design.

## Libraries Used in this Framework
 * D3.js v7 for visualization
 * [axios](https://axios-http.com/docs/intro) for API for dashboard; Flask for server.
 * [pinia](https://pinia.vuejs.org/introduction.html) for store management in Vue.js
 * [Vuetify](https://next.vuetifyjs.com/en/components/all/) for UI that follows Google Material Design 3.
 * [lodash](https://lodash.com/) for utility functions in JavaScript.

## Helpers for D3.js
[There](../../Resources.md) lists some general resources like libraries and tutorials. <br />
Here we dive into more about D3.js, to help you get started with using it.

First of all, reading the following tutorials would help you understand what d3.js is:
[Introduction](https://d3js.org/#introduction),
[Core concepts](https://d3-graph-gallery.com/intro_d3js.html)

On top of the above, here are the most important parts of d3.js, as we often create visual elements from data with these functionalities <br />
  * [Selection](https://www.d3indepth.com/selections/)
  * [Data Joins](https://www.d3indepth.com/datajoins/) <br />

Another important thing is the above mostly cares about *what* to render, so you have to incorporate other functionalities to indicate *where* to render. <br />
* [d3 scale](https://observablehq.com/@d3/introduction-to-d3s-scales) - like mapping functions, e.g., takes data values as input and outputs the coordinates from the viewport.
* [d3 axis](https://observablehq.com/collection/@d3/d3-axis) - responsible for visualizing the scales.
* [Margin conventions](https://observablehq.com/@d3/margin-convention?collection=@d3/d3-axis) - Common practices when setting up scales and axes.
* [Transform in d3](https://www.tutorialspoint.com/d3js/d3js_svg_transformation.htm) - one functionality that we use to re-adjust the positions of the elements on screen.

After creating the visualizations, you can move on to add user interactions, animations and transitions, where often you have to work with event handling in d3.js. <br />
 * [d3 event handling](https://www.stator-afm.com/tutorial/d3-js-mouse-events/) - 90% of the time you will only need `mouseenter`, `mouseon`, `mouseleave`, and `click`.
 * [User interactions](https://www.d3indepth.com/interaction/) - pick, brush, drag, zoom&pan.
   * [Here](https://d3-graph-gallery.com/interactivity.html) provides other examples but using d3 v4, so some syntax is outdated.
 * [d3 animation](https://observablehq.com/@d3/learn-d3-animation)
 * [d3 transition](https://www.d3indepth.com/transitions/)

Here is [a step-by-step example](https://wattenberger.netlify.app/#make-the-interaction-as-easy-as-possible) that implements tooltips with event handling.

[Observable Notebook](https://observablehq.com/) is the notebook paradigm to JavaScript projects, like Jupyter Notebook but in JavaScript. A lot of their notebook create a variety of interactive visualizations with d3.js, **however**, the programming logic would be slightly different because of the unique ecosystem in Observable. 

While Observable provides a [d3.js gallery](https://observablehq.com/@d3/gallery), you can find the same examples but in vanilla JavaScript [here](https://takanori-fujiwara.github.io/d3-gallery-javascript/).

 * [Official d3.js documentation](https://d3js.org/#introduction)
 * [Alternative tutorial for modern d3.js](https://www.d3indepth.com/introduction/)


## Examples in this Framework

Under `./dashboard/src/components` lies 4 components. The first two in the following focuses on d3.js; the last two focuses on Vue.js.
Inside each file you will find more comments on explaining the code/logic.
  * `Example.vue` - A simple scatter plot with d3.js that responds when screen resizes, which also includes some TypeScript expressions.
  * `ExampleWithLegend.vue` - Built upon the above component, but added a legend. 
  * `ExampleWithInteractions.vue` - Built upon the above component, that implements a dropdown menu, communicates with the server on demand, and uses a store along with Composition API. Note that you're not required to do stores or Composition API for the assignment or the final project.
  * `Notes.vue` - showcases how to use Vuetify UI components. This also includes the local state, the state read from the store, and the prop passed down from its parent component.