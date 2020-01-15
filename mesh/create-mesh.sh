aws appmesh create-mesh --mesh-name mymesh

aws appmesh create-virtual-node --cli-input-json file://v1/service/my-vn.json
aws appmesh create-virtual-router --cli-input-json file://v1/service/my-vr.json
aws appmesh create-route --cli-input-json file://v1/service/my-r.json
