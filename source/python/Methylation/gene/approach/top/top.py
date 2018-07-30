from config.config import *
from infrastructure.load.top import *
from gene.approach.top.enet.params import save_params_enet
from gene.approach.top.enet.top import save_top_enet
from gene.approach.top.linreg.top import save_top_linreg
from gene.approach.top.anova.top import save_top_anova
from gene.approach.top.spearman.top import save_top_spearman


def top_proc(config):
    if config.approach_method is Method.enet:
        save_top_enet(config)
    elif config.approach_method is Method.linreg:
        save_top_linreg(config)
    elif config.approach_method is Method.anova:
        save_top_anova(config)
    elif config.approach_method is Method.spearman:
        save_top_spearman(config)

db = DataBaseType.GSE40279
dt = DataType.gene
approach = Approach.top
scenario = Scenario.approach
approach_methods = [Method.anova, Method.enet, Method.linreg, Method.spearman]
approach_gd = GeneDataType.mean
gts = [Gender.any, Gender.M, Gender.F]
geos = [GeoType.islands, GeoType.islands_shores, GeoType.any]


for method in approach_methods:
    print(method.value)
    for gt in gts:
        print(gt.value)
        for geo in geos:
            print(geo.value)

            config = Config(
                db=db,
                dt=dt,
                approach=approach,
                scenario=scenario,
                approach_method=method,
                approach_gd=approach_gd,
                geo=geo,
                gender=gt
            )

            top_proc(config)

