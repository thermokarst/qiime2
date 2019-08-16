# ----------------------------------------------------------------------------
# Copyright (c) 2016-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2 import Artifact, Metadata

import pandas as pd

from .type import IntSequence1, IntSequence2


def ints1_factory():
    return Artifact.import_data(IntSequence1, [0, 1, 2])


def ints2_factory():
    return Artifact.import_data(IntSequence1, [3, 4, 5])


def ints3_factory():
    return Artifact.import_data(IntSequence2, [6, 7, 8])


def concatenate_ints_simple(use):
    '''
    # TODO: anything good we can do with this little bit?
    docstring action
    '''
    use.scope['byod'] = ints1_factory
    use.scope['ints2'] = ints2_factory
    use.scope['this_one_is_important'] = ints3_factory

    use.comment('big data == concatenating ints')
    use.action(
        use.RefAction('dummy_plugin', 'concatenate_ints'),
        use.RefInputs(ints1=use.scope['byod'], ints2=use.scope['ints2'],
                      ints3=use.scope['this_one_is_important'],
                      int1=4, int2=2),
        use.RefOutputs(
            concatenated_ints=use.scope['youre_just_a_copy_of_an_imitation']),
    )
    use.comment('as you can clearly see, p == np')


def concatenate_ints_complex(use):
    use.scope['byod'] = ints1_factory
    use.scope['ints2'] = ints2_factory
    use.scope['this_one_is_important'] = ints3_factory

    use.comment('big data == concatenating ints')
    use.action(
        use.RefAction('dummy_plugin', 'concatenate_ints'),
        use.RefInputs(ints1=use.scope['byod'], ints2=use.scope['ints2'],
                      ints3=use.scope['this_one_is_important'],
                      int1=4, int2=2),
        use.RefOutputs(
            concatenated_ints=use.scope['youre_just_a_copy_of_an_imitation']),
    )
    use.comment('as you can clearly see, p == np')
    use.action(
        use.RefAction('dummy_plugin', 'concatenate_ints'),
        use.RefInputs(ints1=use.scope['youre_just_a_copy_of_an_imitation'],
                      ints2=use.scope['youre_just_a_copy_of_an_imitation'],
                      ints3=use.scope['this_one_is_important'],
                      int1=6, int2=7),
        use.RefOutputs(
            concatenated_ints=use.scope['well_well_well_what_do_we_have_here']),
    )

    # TODO: fix this
    # use.scope['well_well_well_what_do_we_have_here'].assert_has_line_matching(
    #     label='foobarbaz',
    #     path='.*/data/ints.txt',
    #     expression='2\n0\n1\n2',
    # )

    use.comment('fin')


def metadata_factory_a():
    df = pd.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['foo', 'bar', 'baz'],
                      index=pd.Index(['s1', 's2'], name='id'))
    return Metadata(df)


def identity_with_metadata_case_a(use):
    use.scope['ints'] = ints1_factory
    use.scope['md'] = metadata_factory_a
    use.action(
        use.RefAction('dummy_plugin', 'identity_with_metadata'),
        use.RefInputs(ints=use.scope['ints'], metadata=use.scope['md']),
        use.RefOutputs(out=use.scope['ints_out']),
    )


# TODO: fix this
def identity_with_metadata_column_case_a(use):
    pass
#     use.scope.add_artifact('ints', ints1_factory)
#     use.scope.add_metadata('md', metadata_factory_a)
#     use.action(
#         use.RefAction('dummy_plugin', 'identity_with_metadata_column'),
#         use.RefInputs(ints=use.scope['ints'], metadata=use.scope['md'].foo),
#         use.RefOutputs(out='ints_out'),
#     )


def most_common_viz_typical(use):
    use.scope['int'] = ints1_factory

    use.comment('doing things')
    use.action(
        use.RefAction('dummy_plugin', 'most_common_viz'),
        use.RefInputs(ints=use.scope['int']),
        use.RefOutputs(visualization=use.scope['foo']),
    )

    # TODO: fix this
    # use.scope['foo'].assert_has_line_matching(
    #     label='foobarbaz',
    #     path='.*/data/index.tsv',
    #     expression='.*',
    # )