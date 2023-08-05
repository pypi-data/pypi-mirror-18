#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2015 Étienne Loks  <etienne.loks_AT_peacefrogsDOTnet>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# See the file COPYING for details.

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ishtar_common.models import ImporterType, IshtarUser, ImporterColumn,\
    FormaterType, ImportTarget

from archaeological_finds import models

from archaeological_context_records.tests import ImportContextRecordTest, \
    ContextRecordInit

from ishtar_common import forms_common


class ImportFindTest(ImportContextRecordTest):
    test_context_records = False

    fixtures = ImportContextRecordTest.fixtures + [
        settings.ROOT_PATH +
        '../archaeological_finds/fixtures/initial_data-fr.json',
    ]

    def testMCCImportFinds(self, test=True):
        self.testMCCImportContextRecords(test=False)

        old_nb = models.BaseFind.objects.count()
        old_nb_find = models.Find.objects.count()
        MCC = ImporterType.objects.get(name=u"MCC - Mobilier")

        col = ImporterColumn.objects.create(col_number=25,
                                            importer_type_id=MCC.pk)
        formater = FormaterType.objects.filter(
            formater_type='FileFormater').all()[0]
        ImportTarget.objects.create(target='find__image',
                                    formater_type_id=formater.pk,
                                    column_id=col.pk)
        mcc_file = open(
            settings.ROOT_PATH +
            '../archaeological_finds/tests/MCC-finds-example.csv', 'rb')
        mcc_images = open(
            settings.ROOT_PATH +
            '../archaeological_finds/tests/images.zip', 'rb')
        file_dict = {'imported_file': SimpleUploadedFile(mcc_file.name,
                                                         mcc_file.read()),
                     'imported_images': SimpleUploadedFile(mcc_images.name,
                                                           mcc_images.read())}
        post_dict = {'importer_type': MCC.pk, 'skip_lines': 1,
                     "encoding": 'utf-8'}
        form = forms_common.NewImportForm(data=post_dict, files=file_dict,
                                          instance=None)
        form.is_valid()
        if test:
            self.assertTrue(form.is_valid())
        impt = form.save(self.ishtar_user)
        impt.initialize()

        # doing manual connections
        ceram = models.MaterialType.objects.get(txt_idx='ceramic').pk
        glass = models.MaterialType.objects.get(txt_idx='glass').pk
        self.setTargetKey('find__material_types', 'terre-cuite', ceram)
        self.setTargetKey('find__material_types', 'verre', glass)
        impt.importation()
        if not test:
            return
        # new finds has now been imported
        current_nb = models.BaseFind.objects.count()
        self.assertEqual(current_nb, (old_nb + 4))
        current_nb = models.Find.objects.count()
        self.assertEqual(current_nb, (old_nb_find + 4))
        self.assertEqual(
            models.Find.objects.filter(material_types__pk=ceram).count(), 4)
        self.assertEqual(
            models.Find.objects.filter(material_types__pk=glass).count(), 1)
        images = [f.image for f in models.Find.objects.all() if f.image.name]
        self.assertEqual(len(images), 1)


class FindInit(ContextRecordInit):
    test_context_records = False

    def create_finds(self, user=None, data_base={}, data={}, force=False):
        if not getattr(self, 'finds', None):
            self.finds = []
        if not getattr(self, 'base_finds', None):
            self.base_finds = []

        default = {'label': "Base find"}
        if not data_base.get('history_modifier'):
            data_base['history_modifier'] = self.get_default_user()
        if force or not data_base.get('context_record'):
            data_base['context_record'] = self.get_default_context_record(
                force=force)
        default.update(data_base)
        base_find = models.BaseFind.objects.create(**default)
        self.base_finds.append(base_find)

        data["history_modifier"] = data_base["history_modifier"]
        find = models.Find.objects.create(**data)
        find.base_finds.add(base_find)
        self.finds.append(find)
        return self.finds, self.base_finds

    def get_default_find(self):
        return self.create_finds()[0]

    def tearDown(self):
        super(FindInit, self).tearDown()
        if hasattr(self, 'finds'):
            for f in self.finds:
                try:
                    f.delete()
                except:
                    pass
            self.finds = []
        if hasattr(self, 'base_finds'):
            for f in self.base_finds:
                try:
                    f.delete()
                except:
                    pass
            self.base_find = []


class FindTest(FindInit, TestCase):
    fixtures = [settings.ROOT_PATH +
                '../fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../ishtar_common/fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../archaeological_files/fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../archaeological_operations/fixtures/initial_data-fr.json',
                settings.ROOT_PATH +
                '../archaeological_finds/fixtures/initial_data-fr.json',
                ]
    model = models.Find

    def setUp(self):
        self.create_finds(force=True)

    def testExternalID(self):
        find = self.finds[0]
        base_find = find.base_finds.all()[0]
        self.assertEqual(
            find.external_id,
            u"{}-{}".format(
                find.get_first_base_find().context_record.external_id,
                find.label))
        self.assertEqual(
            base_find.external_id,
            u"{}-{}".format(
                base_find.context_record.external_id,
                base_find.label))


class PackagingTest(FindInit, TestCase):
    fixtures = [settings.ROOT_PATH +
                '../fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../ishtar_common/fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../archaeological_files/fixtures/initial_data.json',
                settings.ROOT_PATH +
                '../archaeological_operations/fixtures/initial_data-fr.json',
                settings.ROOT_PATH +
                '../archaeological_finds/fixtures/initial_data-fr.json',
                ]
    model = models.Find

    def setUp(self):
        self.create_finds({"label": u"Find 1"}, force=True)
        self.create_finds({"label": u"Find 2"}, force=True)
        self.basket = models.FindBasket.objects.create(
            label="My basket", user=IshtarUser.objects.get(
                pk=self.get_default_user().pk))
        self.other_basket = models.FindBasket.objects.create(
            label="My other basket", user=IshtarUser.objects.get(
                pk=self.get_default_user().pk))
        for find in self.finds:
            self.basket.items.add(find)
            self.other_basket.items.add(find)

    def testPackaging(self):
        treatment_type = models.TreatmentType.objects.get(txt_idx='packaging')
        treatment = models.Treatment(treatment_type=treatment_type)
        items_nb = models.Find.objects.count()
        treatment.save(user=self.get_default_user(), items=self.basket)
        self.assertEqual(items_nb + self.basket.items.count(),
                         models.Find.objects.count(),
                         msg="Packaging doesn't generate enough new finds")
        # new version of the find is in the basket
        for item in self.basket.items.all():
            self.assertNotIn(
                item, self.finds,
                msg="Original basket have not been upgraded after packaging")
        for item in self.other_basket.items.all():
            self.assertNotIn(
                item, self.finds,
                msg="Other basket have not been upgraded after packaging")
