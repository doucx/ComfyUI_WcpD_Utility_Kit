import { app } from "/scripts/app.js";
import { swapInputs, renameNodeInputs, removeNodeInputs } from "./utils.js"
// CUSTOM_INT, recursiveLinkUpstream, transformFunc, getDrawColor, computeCanvasSize
// MergeStrings
app.registerExtension({
  name: "Comfy.WcpD_Kit.MergeStrings",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "MergeStrings") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function() {
        const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

        // this.setDirtyCanvas(true);
        this.selected = false
        this.index = 1

        this.addInput("text", "STRING")
        this.addInput("text", "STRING")
        renameNodeInputs(this, "text", 0)
        if (this.inputs) {
          this.widgets[this.index].options.max = this.inputs.length - 1
        }
        else {
          this.widgets[this.index].options.max = 0 //this.inputs.length-1
        }

        this.serialize_widgets = true

        this.getExtraMenuOptions = function(_, options) {
          options.unshift(
            {
              content: `insert input above ${this.widgets[this.index].value} /\\`,
              callback: () => {
                this.addInput("text", "STRING")

                const inputLenth = this.inputs.length - 1
                const index = this.widgets[this.index].value

                for (let i = inputLenth; i > index + 1; i--) {
                  swapInputs(this, i, i - 1)
                }
                renameNodeInputs(this, "text", 0)

                this.widgets[this.index].options.max = inputLenth // -1

                this.setDirtyCanvas(true);

              },
            },
            {
              content: `insert input below ${this.widgets[this.index].value} \\/`,
              callback: () => {
                this.addInput("text", "STRING")

                const inputLenth = this.inputs.length - 1
                const index = this.widgets[this.index].value

                for (let i = inputLenth; i > index + 2; i--) {
                  swapInputs(this, i, i - 1)
                }
                renameNodeInputs(this, "text", 0)

                this.widgets[this.index].options.max = inputLenth // -1

                this.setDirtyCanvas(true);
              },
            },
            {
              content: `remove currently selected input ${this.widgets[this.index].value}`,
              callback: () => {
                const index = this.widgets[this.index].value
                removeNodeInputs(this, [index], 0)
                renameNodeInputs(this, "text", 0)

                this.widgets[this.index].options.max = this.inputs.length - 1

              },
            },
            {
              content: "remove all unconnected inputs",
              callback: () => {
                let indexesToRemove = []

                for (let i = 2; i <= this.inputs.length - 1; i++) {
                  if (!this.inputs[i].link) {
                    indexesToRemove.push(i)
                  }
                }

                if (indexesToRemove.length) {
                  removeNodeInputs(this, indexesToRemove, 1)
                  renameNodeInputs(this, "text", 0)
                }

              },
            },
          );
        }

        this.onRemoved = function() {
          // When removing this node we need to remove the input from the DOM
          for (let y in this.widgets) {
            if (this.widgets[y].canvas) {
              this.widgets[y].canvas.remove();
            }
          }
        };

        this.onSelected = function() {
          this.selected = true
        }
        this.onDeselected = function() {
          this.selected = false
        }

        return r
      }
    }
  },

});
