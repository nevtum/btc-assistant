To build, execute the following:

```bash
make -f web_stack.mk build
```

To package and deploy, run the following on the command line

```bash
make -f web_stack.mk package
make -f web_stack.mk deploy
```

To delete stack, run the following command:

```bash
make -f web_stack.mk undeploy
```