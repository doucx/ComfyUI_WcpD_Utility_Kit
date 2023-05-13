import { app } from "/scripts/app.js";
import {CUSTOM_INT, recursiveLinkUpstream, transformFunc, swapInputs, renameNodeInputs, removeNodeInputs, getDrawColor, computeCanvasSize} from "./utils.js"

app.registerExtension({
	name: "Comfy.WcpD_Kit.MergeStrings",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "MergeStrings") {
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
				
				this.setProperty("values", [[0, 0, 0, null]])

				this.selected = false
				this.index = 1

                this.serialize_widgets = true;
                
				CUSTOM_INT(
					this,
					"index",
					0,
					function (v, _, node) {

						let values = node.properties["values"]

						node.widgets[2].value = values[v][0]
						node.widgets[3].value = values[v][1]
						node.widgets[4].value = values[v][2]
					},
					{ step: 10, max: 1 }

				)

				// CUSTOM_INT(this, "x", 0, function (v, _, node) {transformFunc(this, v, node, 0)}, {step: 80})
				// CUSTOM_INT(this, "y", 0, function (v, _, node) {transformFunc(this, v, node, 1)}, {step: 80})
				// CUSTOM_INT(this, "feather", 1, function (v, _, node) {transformFunc(this, v, node, 2)}, {"min": 0.0, "max": 4096, "step": 80, "precision": 0})

				this.getExtraMenuOptions = function(_, options) {
					options.unshift(
						{
							content: `insert input above ${this.widgets[this.index].value} /\\`,
							callback: () => {
								this.addInput("text", "STRING")
								
								const inputLenth = this.inputs.length-1
								const index = this.widgets[this.index].value

								for (let i = inputLenth; i > index+1; i--) {
									swapInputs(this, i, i-1)
								}
								renameNodeInputs(this, "text", 1)

								this.properties["values"].splice(index, 0, [0, 0, 0, null])
								this.widgets[this.index].options.max = inputLenth-1

								this.setDirtyCanvas(true);

							},
						},
						{
							content: `insert input below ${this.widgets[this.index].value} \\/`,
							callback: () => {
								this.addInput("text", "STRING")
								
								const inputLenth = this.inputs.length-1
								const index = this.widgets[this.index].value

								for (let i = inputLenth; i > index+2; i--) {
									swapInputs(this, i, i-1)
								}
								renameNodeInputs(this, "text", 1)

								this.properties["values"].splice(index+1, 0, [0, 0, 0, null])
								this.widgets[this.index].options.max = inputLenth-1

								this.setDirtyCanvas(true);
							},
						},
						{
							content: `remove currently selected input ${this.widgets[this.index].value}`,
							callback: () => {
								const index = this.widgets[this.index].value
								removeNodeInputs(this, [index+1], 1)
								renameNodeInputs(this, "text", 1)
							},
						},
						{
							content: "remove all unconnected inputs",
							callback: () => {
								let indexesToRemove = []

								for (let i = 1; i <= this.inputs.length-1; i++) {
									if (!this.inputs[i].link) {
										indexesToRemove.push(i)
									}
								}

								if (indexesToRemove.length) {
									removeNodeInputs(this, indexesToRemove, 1)
									renameNodeInputs(this, "text", 1)
								}
								
							},
						},
					);
				}

				this.onRemoved = function () {
					// When removing this node we need to remove the input from the DOM
					for (let y in this.widgets) {
						if (this.widgets[y].canvas) {
							this.widgets[y].canvas.remove();
						}
					}
				};
			
				this.onSelected = function () {
					this.selected = true
				}
				this.onDeselected = function () {
					this.selected = false
				}

				return r
			}
		}
    },
	loadedGraphNode(node, _) {
		if (node.type === "MergeStrings") {
			node.widgets[node.index].options["max"] = node.properties["values"].length-1
		}
	},
	
});