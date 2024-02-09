# How to add the algoesup environment to an existing notebook in Datalore

1. In Datalore open the notebook you wish to add the `algoesup` environment to.
1. Click the paper-clip icon (Attached Data) in the left panel.
1. Expand the **Notebook files** folder by clicking on the ">" symbol to the left.
1. Delete the existing `environment.yml` file.
1. Upload the contents of this `Datalore` folder to the remote **Notebook files** folder on Datalore
1. Open a terminal by clicking **Tools > Terminal** from the menu.
1. Run the command `chmod +x init.sh`
1. Run the `init.sh` script with `./init.sh`.
1. Restart the Kernel by clicking **Kernel > Restart kernel**