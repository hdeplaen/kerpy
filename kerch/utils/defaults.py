# coding=utf-8
DEFAULT_KERNEL_TYPE = 'rbf'
DEFAULT_CACHE_LEVEL = {"forward_sample_default_representation": "light",
                       "forward_sample_other_representation": "normal",
                       "forward_oos_default_representation": "heavy",
                       "forward_oos_other_representation": "total",
                       "sample_phi": "light",
                       "sample_C": "light",
                       "sample_K": "light",
                       "Level_I_default_representation": "normal",
                       "Level_I_other_representation": "total",
                       "PPCA_B_primal": "normal",
                       "PPCA_B_dual": "normal",
                       "PPCA_Inv_primal": "normal",
                       "PPCA_Inv_dual": "normal",
                       "KPCA_total_variance_default_representation": "normal",
                       "KPCA_total_variance_other_representation": "total",
                       "Level_subloss_default_representation": "normal",
                       "Level_subloss_other_representation": "total",
                       "sample_transform": "none",
                       "kernel_explicit_transform": "none",
                       "kernel_implicit_transform": "none",
                       "Wasserstein_kernel_dist": "normal",
                       "transform_sample_data_default": "light",
                       "transform_sample_data_nondefault": "normal",
                       "transform_sample_statistics_default": "light",
                       "transform_sample_statistics_nondefault": "light",
                       "transform_oos_data_level_default": "heavy",
                       "transform_oos_data_level_nondefault": "total",
                       "transform_oos_statistics_default": "normal",
                       "transform_oos_statistics_nondefault": "heavy",
                       "_poly_explicit_fun": "light",
                       "_nystrom_elements": "light"
                       }
