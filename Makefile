#Modificar ruta al generador
GENERATOR_DIR = ../msdir/ms


PYTHON = python
INSTANCE_SCRIPT = experiments/generate_instances.sh
RUN_EXP_SCRIPT = experiments/run_exp.sh
SRC_DIR = src
INSTANCE_DIR = instances
SCRIPT_DIR = src
RESULTS_DIR = experiments/results
CSV_DIR = results

# Comandos
generate_instances:
	bash $(INSTANCE_SCRIPT) $(GENERATOR_DIR) $(INSTANCE_DIR)

run_experiments:
	bash $(RUN_EXP_SCRIPT) $(INSTANCE_DIR) $(RESULTS_DIR) $(SCRIPT_DIR)
	bash $(CSV_DIR)/create_csv.sh $(RESULTS_DIR) $(CSV_DIR)

clean:
	rm -f experiments/results/f1/*.txt
	rm -f experiments/results/f2/*.txt
	rm -f $(INSTANCE_DIR)/*.txt

.PHONY: generate_instances run_experiments




